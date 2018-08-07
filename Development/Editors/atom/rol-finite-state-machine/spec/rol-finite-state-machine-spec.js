'use babel';

import RolFiniteStateMachine from '../lib/rol-finite-state-machine';

// Use the command `window:run-package-specs` (cmd-alt-ctrl-p) to run specs.
//
// To run a specific `it` or `describe` block add an `f` to the front (e.g. `fit`
// or `fdescribe`). Remove the `f` to unfocus the block.

describe('RolFiniteStateMachine', () => {
  let workspaceElement, activationPromise;

  beforeEach(() => {
    workspaceElement = atom.views.getView(atom.workspace);
    activationPromise = atom.packages.activatePackage('rol-finite-state-machine');
  });

  describe('when the rol-finite-state-machine:toggle event is triggered', () => {
    it('hides and shows the modal panel', () => {
      // Before the activation event the view is not on the DOM, and no panel
      // has been created
      expect(workspaceElement.querySelector('.rol-finite-state-machine')).not.toExist();

      // This is an activation event, triggering it will cause the package to be
      // activated.
      atom.commands.dispatch(workspaceElement, 'rol-finite-state-machine:toggle');

      waitsForPromise(() => {
        return activationPromise;
      });

      runs(() => {
        expect(workspaceElement.querySelector('.rol-finite-state-machine')).toExist();

        let rolFiniteStateMachineElement = workspaceElement.querySelector('.rol-finite-state-machine');
        expect(rolFiniteStateMachineElement).toExist();

        let rolFiniteStateMachinePanel = atom.workspace.panelForItem(rolFiniteStateMachineElement);
        expect(rolFiniteStateMachinePanel.isVisible()).toBe(true);
        atom.commands.dispatch(workspaceElement, 'rol-finite-state-machine:toggle');
        expect(rolFiniteStateMachinePanel.isVisible()).toBe(false);
      });
    });

    it('hides and shows the view', () => {
      // This test shows you an integration test testing at the view level.

      // Attaching the workspaceElement to the DOM is required to allow the
      // `toBeVisible()` matchers to work. Anything testing visibility or focus
      // requires that the workspaceElement is on the DOM. Tests that attach the
      // workspaceElement to the DOM are generally slower than those off DOM.
      jasmine.attachToDOM(workspaceElement);

      expect(workspaceElement.querySelector('.rol-finite-state-machine')).not.toExist();

      // This is an activation event, triggering it causes the package to be
      // activated.
      atom.commands.dispatch(workspaceElement, 'rol-finite-state-machine:toggle');

      waitsForPromise(() => {
        return activationPromise;
      });

      runs(() => {
        // Now we can test for view visibility
        let rolFiniteStateMachineElement = workspaceElement.querySelector('.rol-finite-state-machine');
        expect(rolFiniteStateMachineElement).toBeVisible();
        atom.commands.dispatch(workspaceElement, 'rol-finite-state-machine:toggle');
        expect(rolFiniteStateMachineElement).not.toBeVisible();
      });
    });
  });
});
