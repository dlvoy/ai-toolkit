# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

## 2026-08-23

### Added

- Date-based versioning in `YYYY-MM-DD` form, alongside the existing `YYYYMMDD` and SemVer
  schemes.
- Scheme detection now falls back to the changelog's own release headers when a repo has no
  tags, so a project that dates its changelog and never tags is handled correctly.
- Pointer to the external `unslop` skill, for stripping the tells that make agent output
  read as machine-written.
- A prompt for the versioning scheme, and for whether to create a `CHANGELOG.md`, shown when
  a repo has no tag, changelog, or manifest version to infer either from. Both skills used to
  assume SemVer and create the file uninvited.

### Changed

- `commit` no longer pushes anything, including a tag it creates via `as <version>`. Commits
  accumulate locally until you push them yourself or run `commit-tag-push`.
- `commit-and-tag` is now `commit-tag-push`, and pushes the new tag together with every
  commit still waiting on the branch.
- Commit bodies now follow a fixed shape: a one or two sentence summary, then a flat list of
  the changes that matter, with trivial work left out.
- Date-based changelogs no longer use an `Unreleased` section. Entries go straight into the
  section for today's date, and several commits on the same day accumulate into one section.
- Scheme detection now reads a manifest's `version` field as a SemVer signal, so a
  `package.json` or `Cargo.toml` is enough to identify the scheme without a tag or changelog.

### Fixed

- Both skills failing outright in a repo with no commits yet. Every command that reads `HEAD`
  is now guarded, and the initial commit gets a listing of the files it would contain in place
  of a diff that cannot be produced.
- `commit-tag-push` writing a commit and a tag before discovering the repo has no remote to
  push them to. It checks for one before staging anything.
