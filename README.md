# stash

Preset storage, recall and morphing for Pure Data.

Save the state of your sliders, number boxes, lists and arrays into slots, jump or glide between them, and morph between several presets at once. Presets are saved as plain text files.

stash comes in two tiers with the same objects:

- **Vanilla tier**: pure Pd abstractions, no externals needed. Works in Pd vanilla 0.54+ and plugdata.
- **External tier** (planned): compiled drop-in replacement, faster and with live patch scanning.

## Install

In Pd: Help > Find externals, search for `stash`, install.

Then use objects with the library prefix:

```
[stash/bank synth]
[stash/param synth cutoff 20 20000 exp]
```

## Objects

| Object | What it does |
| --- | --- |
| `stash/bank` | Manager: store, recall, glide, morph, save and load presets |
| `stash/param` | Registers one parameter (float, list or symbol) |
| `stash/array` | Stores and recalls a whole array |
| `stash/morph` | XY morph between four presets |
| `stash/ui` | Ready-made preset panel |

See each object's help file for details.

## Status

Early development. Vanilla tier first, external tier later.

## License

BSD 3-Clause. See LICENSE.

## Author

Sofia Vallejo Budziszewski, IEM Graz
