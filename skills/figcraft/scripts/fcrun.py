"""Run FigCraft commands on a design file without the app window.

    python fcrun.py FILE script.json [--save]      one script, results as JSON lines
    python fcrun.py FILE --tree NODE_ID [DEPTH]    print a node's subtree (ids, types, names, texts)

As a module: `from fcrun import FigCraft; fc = FigCraft(FILE); fc.run([...], save=True)`.

A script is a list of {"command": id, "params": {...}} and runs as one all-or-nothing step.
Steps can't refer to an earlier step's result, so work in phases: create or duplicate and save,
read the new ids from the results, then edit them in the next run.
"""
import json
import os
import subprocess
import sys
import tempfile

CLI = os.environ.get("FIGCRAFT_CLI", r"C:\Program Files\FigCraft\figcraft-cli.exe")


class FigCraft:
    def __init__(self, file, cli=CLI):
        self.file, self.cli = os.path.abspath(file), cli

    def run(self, steps, save=False):
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(steps, f, ensure_ascii=False)
        try:
            args = [self.cli, "run", "--no-system-fonts", "--in", self.file, path]
            if save:
                args += ["--out", self.file]
            out = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
        finally:
            os.remove(path)
        if out.returncode:
            raise RuntimeError(out.stderr.strip() or out.stdout.strip())
        return [json.loads(line) for line in out.stdout.splitlines() if line.strip()]

    def tree(self, root, depth=6):
        """{id: outline} for root and every descendant with children, `depth` levels down."""
        out, level = {}, [int(root)]
        for _ in range(depth + 1):
            if not level:
                break
            res = self.run([{"command": "node.get", "params": {"id": str(i), "outline": True}} for i in level])
            nxt = []
            for i, r in zip(level, res):
                out[i] = r["result"]
                nxt += [c["id"] for c in r["result"].get("children", []) if c.get("childCount")]
            level = nxt
        return out

    def show(self, root, depth=6):
        t = self.tree(root, depth)

        def walk(i, ind):
            for c in t[i].get("children", []):
                text = c.get("characters")
                print("  " * ind + f'{c["id"]} {c["type"]} "{c["name"][:40]}"' + (f" = {text[:50]!r}" if text else ""))
                if c["id"] in t:
                    walk(c["id"], ind + 1)

        walk(int(root), 0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    fc = FigCraft(sys.argv[1])
    if sys.argv[2] == "--tree":
        fc.show(sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 6)
    else:
        steps = json.load(open(sys.argv[2], encoding="utf-8"))
        for r in fc.run(steps, "--save" in sys.argv):
            print(json.dumps(r, ensure_ascii=False))
