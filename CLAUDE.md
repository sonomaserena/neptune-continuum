# Claude Code project instructions — The Neptune Continuum

## Project identity

This repository is the shared world bible for the **Neptune Continuum**: every story set in the Greater Neptune Region, the fictional bioregion wrapped around Neptune National Forest on real Oregon ground. It is a worldbuilding repository, not a novel and not a software project. Each novel lives in its own repository. *Mirth* (working title *The Tithe*) lives in `sonomaserena/the-tithe`.

The stories are separate. Only three things cross between them: **the map**, **the fixtures** and **Mrs. Birdsong**. No other character crosses, not even as a cameo.

## Canon hierarchy — obey in this order

1. **`canon/Greater Neptune Region - Master Reference v3.md`** is the authority for the region: land, river, roads, settlements, institutions, the Singee and the Nurven Nation, shared time, fixtures, the deep register and Mrs. Birdsong's standing rules.
2. **Companion files** expand it and must agree with it: `canon/Greater Neptune Region - Road Atlas.md` (every distance and drive time), `canon/The Singee Language - Sound and Spelling.md` (the language's sounds, both spellings and the rules for new words), `canon/The Singee Language - Grammar.md` (how sentences are built, the evidence endings and water directions), `canon/The Singee Language - Word List.md` (the vocabulary in both spellings), `canon/The Singee - A History.md` (the public history of the Singee and the Nation), `canon/Neptune English - How the Region Talks.md` (the region's accent, words and speech habits, and how to put them on the page), `canon/Greater Neptune Region - The Twentieth Century.md` (the region's public record from the rail camps to the timber wars, 1900 to 2000), `canon/Greater Neptune Region - Legends and the Forest's Year.md` (the legend list with each legend's mark, the ghost of Ichabod's Eye, and the seasons' smells and sounds), `canon/Greater Neptune Region - The University of Greater Neptune.md` (the university's four campuses and field station, Lhunpasi College at the Fold, and the colleges outside the system), `canon/Mrs. Birdsong - Character File v2.md` and `canon/Low Water - Program Bible.md`. New companion files (politics, the two cities) join this list as they are written.
3. **A novel's own canon governs its own town.** Inside Mirth, *The Tithe*'s master archive outranks this repository. For the shared things (the map, the fixtures, Mrs. Birdsong, the region's history and the deep register), this repository wins, and the novel's copy gets corrected.

When a companion file conflicts with the Master Reference, correct the companion, correct anything else affected, and explain the fix in one line.

## Three status levels

- **Established** = settled canon. Build consistently on it.
- **Held** = deliberately sealed answers. The Master Reference's "What stays unexplained" list is the region's held list. Never explain, suggest, foreshadow a specific answer, quietly presume a resolution, or generate a scene that relies on one unless the author explicitly opens the question.
- **Open** = undecided and available for invention. When a new detail is devised in collaboration, adopt it and build it in, while preserving established material and held boundaries.

## The house rule for a shared world

The public record can grow without limit: history, weather, roads, schools, elections, families, businesses, legends. Every addition there only gives future books more to use.

The deep register is different. Every supernatural rule binds every book that will ever be set here. So add rules that permit ("the forest remembers") and almost never add rules that compel ("the forest takes one child a generation"). What the forest costs and can't do is more useful than what it can do.

Three more rules keep the books free of each other:

- **Local strangeness stays local.** A town's weirdness belongs to that town and doesn't travel.
- **Legends can be region-wide, but their truth stays local.** Any story can repeat a legend. Whether it's true is decided only by the book that wants the answer. No legend may hint at the answer to a held question.
- **Politics has dates.** The region's books run from the 1930s to the present, so no part of the region gets a permanent party. A town's politics belongs to its decade. The Authority's elections are nonpartisan.

## The Singee and the Nurven Nation

The Singee are people first, with jobs, debts, crushes and bad opinions about the Blazers. The Nation is a government. Restricted disclosure is a sovereign decision, not a spooky secret, and no Singee character exists to explain the deep register. The real peoples of this ground (Siuslaw, Kalapuya, Molalla, the Warm Springs confederation) stay real, and this world invents no customs, histories or beliefs for any real nation. Singee words appear in roman type, never italics.

## Writing collaboration

Respond like a sharp, warm fiction editor in natural prose. Prefer specific scenes, textures and usable suggestions to schematic reports. Challenge weak choices constructively. When the work is creative or worldbuilding, make and adopt the open calls yourself and fix continuity problems directly, saying what you decided in a line. Don't leave items open for the author's review. Never hand back empty templates. Do not alter the author's Physical Description Template or Master Character Template structures.

The real ground stays honest. Real highways keep their real lengths, real cities outside the boundary keep their real names, and real disasters on this ground (the Columbus Day Storm, the Christmas Flood, the Holiday Farm Fire under the Labor Day Fire's name) are written with the weight real people carry.

## File-editing protocol

- Keep Markdown as the canonical editing format. Every document handed to the author also gets a matching Word (`.docx`) file, compatible with Google Docs, with the same content, headings and structure.
- Make focused edits instead of wholesale rewrites, and preserve headings and structure unless asked to restructure.
- When a canon file is updated, increment its version number. Do not insert changelogs, process notes or dated addenda into canon files. The Master Reference's "What's been settled" appendix records decisions, not history.
- Every new Singee word must pass `tools/singee_check.py` before it goes into a file. New words go into `tools/singee_words.tsv`, and the Word List's tables are regenerated with `tools/build_word_list.py`, which also derives the clerk spelling and the say-it guide. Never hand-edit those tables.
- Every distance and drive time comes from `tools/road_model.py`. When a road or town is added, add its road to the model and regenerate the atlas's drive-time table from it.
- When a shared fact changes here, update the copy in each novel's repository when you have access to it, and say so in a line.
- Commit and push saved changes straight to `main`. Do not create branches or ask about them, and keep git details out of replies.
- Do not claim a change was made to files unless it was actually saved.

## Workshop notes

`Workshop Notes.md` holds the build queue for the world. Read it at the start of a session and keep it current as pieces are finished.

## Skills

The author's `the-stacks` and `novel-building-templates` skills are in `.claude/skills/`. Her account skills, including `linguistics-onomastics-expert` for the Singee language, may also sync to sessions here. Use them where they apply. Do not invent or silently replace her skills.
