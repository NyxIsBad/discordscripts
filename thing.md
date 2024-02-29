`\{(.*?)\}` -> for removing stuff in selectorplaceholders

`[^\x00-\x7F]+` -> removing non ascii chars

`e.exports = \{(.*?)\}` -> classes.js stuff

rename addon script to main and run `npm run addons`
- `cit.py` - check if a list of newline separated classes is in the .css files
    - returns fail.txt
- `it.py` - check if a list of newline separated classes are in the theme file 
    - returns fail_in_theme.txt
- `diff.py` - accepts .diff file generated with `git diff commit1^..commit2 --diff-algorithm=patience > classesjs.diff` of the classes.js file. Use the BD-Addons repo in /Desktop
    - You generate the diff file, then enter it in notepad ++, mark classes.js stuff, then search > bookmark > remove non bookmarked lines
    - Run `python diff.py --help` to see help