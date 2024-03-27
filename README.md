# Discord Scripts
The repo is currently serving the diff between the `1b63a9f` and `ad2007f` commits from Sarah's [BD Addons](https://github.com/itmesarah/classchanges/commits/main/discordclasses.js)

SyndiShanX also has his [own scripts](https://github.com/SyndiShanX/Update-Classes) which produce very similar results to mine but use a different methodology. In fact I have added a CLI flag to my script that generates results in syndishanx's style. Note that the script is really flawed and misses a lot of class rerolls! It prioritizes accuracy over completeness, so it will not catch everything.

- `cit.py` - check if a list of newline separated classes is in the .css files
    - returns fail.txt
- `it.py` - check if a list of newline separated classes are in the theme file 
    - returns fail_in_theme.txt
- `diff.py` - accepts .diff file generated with 
    ```git
    git diff commit1..commit2 --word-diff=porcelain ./discordclasses.js > classesjs.diff
    ``` 
    OR 
    ```git
    git diff commit1..commit2 --diff-algorithm=histogram ./discordclasses.js > classesjs.diff 
    ```
    of the classes.js file. Currently using the BD-Addons repo
    - Run `python diff.py --help` to see command flags. Syndi output requires diff output first
    - Requires pandas

Regex Patterns:
`\{(.*?)\}` -> for removing stuff in selectorplaceholders

`[^\x00-\x7F]+` -> removing non ascii chars

`e.exports = \{(.*?)\}` -> classes.js stuff
