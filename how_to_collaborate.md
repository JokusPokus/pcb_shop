# Collaboration guidelines

## Issue tracking
* We use GitHub's issue tracking functionality, namely the inbuilt Kanban board.

## Git
* Keep master clean, always work in feature branches.
* Avoid working on the same branch simultaneously. If not avoidable, communicate very well. 
* Each pull request is reviewed by a peer, and suggested changes are checked by the original author, who then merges 
the feature branch into the master.
* We will follow [this workflow guideline](https://sandofsky.com/workflow/git-workflow/).

## Code reviews
* No single line of code is merged into master without a peer review.

Code reviews should look at:

* Design: Is the code well-designed and appropriate for your system?
* Functionality: Does the code behave as the author likely intended? Is the way the code behaves good for its users?
* Complexity: Could the code be made simpler? Would another developer be able to easily understand and use this code when they come across it in the future?
* Tests: Does the code have correct and well-designed automated tests?
* Naming: Did the developer choose clear names for variables, classes, methods, etc.?
* Comments: Are the comments clear and useful?
* Style: Does the code follow our style guides?
* Documentation: Did the developer also update relevant documentation?

## Commit messages
* We will follow [these guidelines](https://chris.beams.io/posts/git-commit/).

## Style
* We will follow the [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/) for Python code.

## Testing
* We use the PyTest testing framework.
* Each pull request should contain relevant automated tests.
* [Relevant Test Definition]

## Communication
* We will reserve time for a weekly check-up and parallel or partner coding sessions.
* We pledge to respond to project-related requests within 24 hours.