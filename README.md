# Discord Scripts & Use
The repo is currently serving the diff between the `6b9dd01` and `7583133` commits from Sarah's [BD Addons](https://github.com/itmesarah/classchanges/commits/main/discordclasses.js). You can use Ames' [implementation script](https://github.com/accrazed/far) to use it with the served .diff files, or you can call diff.py with the replace flag, which accepts a file and replaces classes based on a classesjs input

# Structure: 
- `classes_mapping.csv contains` csv data that's for other programs to interpret
- `classes_mapping.diff contains` the above data in .diff format
- `classes_mapping_selectors.diff` contains diff data that may include manually found class changes. It's important to take the union of this and `classes_mapping.diff`, because the script is in no way complete (it catches about 90% of changes but can easily miss some of the most critical classes due to uncertainty about class mappings - guaranteed correctness is more important than completeness)
- Almost all of the other files are completely random scripts (or related artifacts) developed for day to day maintenance of the Clearvision Theme, which I'm the developer of. You can ignore those.

# Credits!
- Massive credit to sarah for keeping a history of the discord js file so this is possible. It's probably the one file that can produce a reasonable diff
- Ames has made a script to implement the actual `.diff`s  [here](https://github.com/accrazed/far). Please go check it out, it's incredibly useful
- SyndiShanX also has his [own scripts](https://github.com/SyndiShanX/Update-Classes) which produce very similar results to mine but use a slightly different methodology. In fact I have added a CLI flag to my script that generates results in syndishanx's style. Note that the script is really flawed and misses a lot of class rerolls! It prioritizes accuracy over completeness, so it will not catch everything. Consequently, I may also provide another .diff file that has critical classes that most themes might use, but this is made manually and takes a while to sort out.

# Docs
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

# Useful Patterns:
`\{(.*?)\}` -> for removing stuff in selectorplaceholders

`[^\x00-\x7F]+` -> removing non ascii chars

`e.exports = \{(.*?)\}` -> classes.js stuff

`\r\n\r\n \..*` -> classescss.diff stuff

`git diff --word-diff=porcelain --no-index ./sources/14.css ./sources/15reroll.css > classescss.diff`
