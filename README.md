# Discord Scripts
The repo is currently serving the diff between the `00541a0` and `80a7115` commits from Sarah's [BD Addons](https://github.com/ItMeSarah/BD-Addons/commits/main/DiscordClasses/classes.js)

- `cit.py` - check if a list of newline separated classes is in the .css files
    - returns fail.txt
- `it.py` - check if a list of newline separated classes are in the theme file 
    - returns fail_in_theme.txt
- `diff.py` - accepts .diff file generated with `git diff commit1^..commit2 --word-diff=porcelain > classesjs.diff` OR `git diff commit1^..commit2 --diff-algorithm=histogram > classesjs.diff` of the classes.js file. Currently using the BD-Addons repo
    - You generate the diff file, then do some basic beginner editing with notepad++, mark classes.js stuff, then search > bookmark > remove non bookmarked lines
    - Run `python diff.py --help` to see help
    - Requires pandas, tqdm, psutil (last 2 are for debugging reasons)

Regex Patterns:
`\{(.*?)\}` -> for removing stuff in selectorplaceholders

`[^\x00-\x7F]+` -> removing non ascii chars

`e.exports = \{(.*?)\}` -> classes.js stuff
