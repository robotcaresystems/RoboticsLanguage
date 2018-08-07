const {CompositeDisposable} = require('atom')
const vis = require('vis')

module.exports = {
  subscriptions: null,

  activate () {
    this.subscriptions = new CompositeDisposable()
    this.subscriptions.add(atom.commands.add('atom-workspace',
      {'rol-finite-state-machine:insert': () => this.insert()})
    )
  },

  deactivate () {
    this.subscriptions.dispose()
  },

  insert() {

    // main element
    main_element = document.createElement('div');

    // button to start plot
    button_element = document.createElement('button');
    button_element.innerHTML = 'Show Finite State Machine';
    button_element.onclick = function(){

      var nodes = [
          {id: 1, label: 'Node 1'},
          {id: 2, label: 'Node 2'},
          {id: 3, label: 'Node 3'},
          {id: 4, label: 'Node 4'},
          {id: 5, label: 'Node 5'}
        ];
        // create an array with edges
        var edges = [
          {from: 1, to: 2, label: 'edgeLabel'},
          {from: 1, to: 3, label: 'edgeLabel'},
          {from: 2, to: 4},
          {from: 2, to: 5}
        ];
        // create a network
        var container = document.getElementById('visualization');
        var data = {
          nodes: nodes,
          edges: edges
        };
        var options = {
        };
      var network = new vis.Network(container, data, options);
      network.setSize(600,600);
     };

    // the finite state machine graphics
    vis_element = document.createElement('div')
    vis_element.setAttribute('id','visualization')

    // join everything
    main_element.appendChild(button_element)
    main_element.appendChild(vis_element)

    // create decoration
    editor = atom.workspace.getActiveTextEditor()
    marker = editor.markScreenPosition(editor.getCursorBufferPosition())
    editor.decorateMarker(marker, {type: 'block', position: 'before', item: main_element, size:'600'})

  }

}
