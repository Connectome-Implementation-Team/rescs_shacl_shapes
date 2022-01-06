# Code Review Process

## Definition of a Code Review

A person or several persons other than the author of a piece of a code assess its quality and request improvements or changes if necessary.
Only after a successful review process - all issues raised by the reviewers have been adequately addressed by the code's author - code should be merged into a repository's main branch.

## Purpose and Goal of Code Reviews

A code review assures that new code or changes to existing code meet the requirements of a given task (requested feature, bug fix).
It also reduces the risk of new bugs introduced by new code or changes made to existing code.
Code reviews have the effect that knowledge of the code base is shared across the whole development team.

## Extent of Code Reviews

- Check for things that are obviously wrong or missing.
- Check that the code's quality is sufficient for the purpose it should fulfil (requested feature, bug fix).
- Assure that the code can be understood by others than its creator and is documented.
- Ask questions if something is not clear or request improvements.
- Check that test cases were added and/or adapted if automated tests are required.

## Code Reviews in Practice (GitHub, GitLab)

Code reviews are conducted on pull or merge requests (GitHub, GitLab).
Such a request consists of code changes made on a separate branch
that is to be merged back into a git repository's main branch.

During a code review
- Add specific comments directly to the affected lines of code
- Add general comments summarising your overall understanding

The code's author can then directly react to these comments.
If comments request changes, then the code's author should either mention the commits
that implement those requested changes, e.g., "done in xy"
or link to issues that were created to address those requested changes in the future.

Once all issues raised by the reviewers haven been adequately addressed,
the reviewers should approve the request. Merging should be left to the request's author.

## Planning/Scheduling of Code Reviews

Proper code reviews need time.

Ideally a pull or merge request addresses a specific purpose and is not too extensive.
The potential code reviewers should be given notice of an upcoming pull or merge request in advance
so they can schedule it.

The author should make sure that the code is ready to be reviewed before requesting a code review.

## References

- https://smartbear.com/learn/code-review/guide-to-code-review-process/
- https://www.atlassian.com/de/agile/software-development/code-reviews
- https://google.github.io/eng-practices/review/
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews
