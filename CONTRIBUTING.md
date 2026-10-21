# Contributing

Thanks for helping. The most useful contributions right now:

1. **Benchmarks** for the open questions in `docs/09-open-questions-and-benchmarks.md`, always with the method.
2. **Unreal Engine version reports** for `unreal/import_camera_csv.py`: engine version, what worked, what broke.
3. **Matting comparisons** on hair, wigs, lace and props, with licence notes for each model.
4. **Translations** of the docs (Thai, Japanese, Chinese, Spanish, ...). Put them in `docs/<lang>/`.
5. **New tools** for the MCP server, with tests.

## Rules

- Code: run `pytest` before a pull request. New tools need a test, ideally on synthetic footage generated in the test (see `tests/test_media.py`).
- Tools call external programs with argument lists, never a shell string.
- No ripped or unlicensed assets: game models, logos, music, voice lines. Sample footage must be your own, of people who consented, and released under CC BY 4.0 or similar.
- Say what is tested and what is a hypothesis. Docs mark each page's status.

## Licence of contributions

By contributing you agree your code is released under MIT and your docs and skills under CC BY 4.0.
