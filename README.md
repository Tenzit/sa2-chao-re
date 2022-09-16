# sa2-chao-re

This repo contains scripts that reverse-engineer parts of the chao code
in Sonic Adventure 2: Battle.

## Requirements

This project was developed on Linux and uses python3-venv to manage
dependencies.
```bash
sudo apt install python3-venv
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Usage

### chao_gen.py

`chao_gen.py` will search for a chao with given stats and output the
rng call that said chao would be generated on.

```bash
./chao_gen.py --min-stats 2 1 5 3 2 --rng-iters 200
RNG Calls: 147 Seed: 0x5c58fca5 Method C: Swim 2, Fly 1, Run 5, Power 3, Stam 2, Int 0, Luck 0, Unknown 1
```

See `chao_gen.py --help` for a full list of options
