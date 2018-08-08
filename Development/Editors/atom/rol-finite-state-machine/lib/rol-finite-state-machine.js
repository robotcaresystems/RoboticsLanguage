const {CompositeDisposable} = require('atom')
const vis = require('vis')


module.exports = {
  subscriptions: null,

  // vis graph structures
  network_data: null,
  network: null,

  // this runs when atom starts
  activate () {

    this.subscriptions = new CompositeDisposable()

    // add a command to atom
    this.subscriptions.add(atom.commands.add('atom-workspace',
      {'rol-finite-state-machine:insert': () => this.insert()})
    )

    // ad a callback that is executed when a file is opened
    this.subscriptions.add(atom.workspace.observeTextEditors(editor => {

      console.log('trying to match...')

      // search for the FiniteStateMachine tag
      editor.scan(new RegExp('FiniteStateMachine[\s|\n]*<{(.*|\n)*?}>', 'g'), iterator => {

        console.log('Match! ' + iterator.match);
        console.log(iterator)
        console.log(iterator.range.start)

        // create a button with an eye icon
        button_view = document.createElement('button');
        button_view.setAttribute('class','btn btn-default tool-bar-btn icon-eye')

        // add the button right before the tag was found
        marker = editor.markScreenPosition(iterator.range.start)
        editor.decorateMarker(marker, {type: 'block', position: 'before', item: button_view, size:'600'})

        // hide the text
        // editor.foldSelectedLines(iterator.range)

      });
    }));



  },
  deactivate () {
    this.subscriptions.dispose()
  },


  insert() {

    // main element
    main_element = document.createElement('div');


    // <i class="arrow alternate circle right outline icon"></i>
    // <i class="arrow alternate circle right icon"></i>
    //<i class="plus circle icon"></i>
    // <i class="arrow alternate circle right outline icon"></i>


    // button to start plot
    button_view = document.createElement('button');
    button_view.setAttribute('class','btn btn-default tool-bar-btn icon-eye')

    button_add_state = document.createElement('button');
    button_add_state.setAttribute('class','btn btn-default tool-bar-btn icon-diff-added')

    button_add_arc = document.createElement('button');
    button_add_arc.setAttribute('class','btn btn-default tool-bar-btn icon-diff-renamed')

    button_view.onclick = function(){
      if( this.network_data == null)
      {

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
          this.network_data = {
            nodes: nodes,
            edges: edges
          };
          var options = {
            manipulation: {
              enabled: true
            },
          //   interaction: {
          //   navigationButtons: true,
          //   keyboard: true
          // }
          };
        this.network = new vis.Network(container, this.network_data, options);
        this.network.setSize(600,600);
      }
      else {
        var x = document.getElementById('visualization');
        if (x.style.display === "none") {
              x.style.display = "block";
          } else {
              x.style.display = "none";
          }      }
     };

    // the finite state machine graphics
    vis_element = document.createElement('div')
    vis_element.setAttribute('id','visualization')

    // join everything
    main_element.appendChild(button_view)
    main_element.appendChild(button_add_state)
    main_element.appendChild(button_add_arc)
    main_element.appendChild(vis_element)

    // create decoration
    editor = atom.workspace.getActiveTextEditor()
    marker = editor.markScreenPosition(editor.getCursorBufferPosition())
    editor.decorateMarker(marker, {type: 'block', position: 'before', item: main_element, size:'600'})

  },





}
