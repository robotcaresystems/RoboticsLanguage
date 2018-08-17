const {
  CompositeDisposable
} = require('atom')
const vis = require('vis')
var dialogs = require('dialogs')() //Needed for electron dialogs

var id = 1;
var edgeId = 1;
module.exports = {
  subscriptions: null,

  // vis graph structures
  network_data: null,
  network: null,

  // this runs when atom starts
  activate() {

    this.subscriptions = new CompositeDisposable()

    // add a command to atom
    this.subscriptions.add(atom.commands.add('atom-workspace', {
      'rol-finite-state-machine:insert': () => this.insert()
    }))

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
        button_view.setAttribute('class', 'btn btn-default tool-bar-btn icon-eye')



        // add the button right before the tag was found
        marker = editor.markScreenPosition(iterator.range.start)
        editor.decorateMarker(marker, {
          type: 'block',
          position: 'before',
          item: button_view,
          size: '1000'
        })

        // hide the text
        // editor.foldSelectedLines(iterator.range)

      });
    }));



  },
  deactivate() {
    this.subscriptions.dispose()
  },


  insert() {

    // main element
    main_element = document.createElement('div');
    // create an array with nodes
    nodesArray = [{
      id: 1,
      label: '1'
    }, ];
    nodes = new vis.DataSet(nodesArray);

    // create an array with edges
    edgesArray = [];
    edges = new vis.DataSet(edgesArray);

    //Defining buttons
    button_view = document.createElement('button');
    button_view.setAttribute('class', 'btn btn-default tool-bar-btn icon-eye')

    button_add_state = document.createElement('button');
    button_add_state.setAttribute('class', 'btn btn-default tool-bar-btn icon-diff-added')

    button_add_arc = document.createElement('button');
    button_add_arc.setAttribute('class', 'btn btn-default tool-bar-btn icon-diff-renamed')

    button_remove_edge = document.createElement('button');
    button_remove_edge.setAttribute('class', 'btn btn-default tool-bar-btn icon-x')

    button_remove_node = document.createElement('button');
    button_remove_node.setAttribute('class', 'btn btn-default tool-bar-btn icon-diff-removed')

    button_generate_rol = document.createElement('button');
    button_generate_rol.setAttribute('class', 'btn btn-default tool-bar-btn icon-zap')


    var transitions = edges.size;

    button_view.onclick = function() {
      if (this.network_data == null) {
        // create a network
        var container = document.getElementById('visualization');
        var data = {
          nodes: nodes,
          edges: edges
        };
        var options = {
          edges: {
            arrows: 'to',
            color: {
              highlight: 'green',
            },
            font: '12px arial #ff0000',
            scaling: {
              label: false,
            },
            shadow: true,
            smooth: true,
          },
          nodes: {
            color: {
              highlight: 'red',
            }
          },
          layout: {
            randomSeed: 1
          },
        };
        network = new vis.Network(container, data, options);
      } else {
        var x = document.getElementById('visualization');
        if (x.style.display === "none") {
          x.style.display = "block";
        } else {
          x.style.display = "none";
        }
      }
    };
    button_add_arc.onclick = function() {
      var name, from, to;
      console.log("tring to add transition state...");
      dialogs.prompt('From node id:', function(ok) {
        console.log(ok);
        if (!ok) {
          console.log("typedef undefined....")
          return;
        }
        from = ok
        // console.log('ID:', ok)
        dialogs.prompt('To node id:', function(ok) {

          console.log('Label:', ok)
          if (!ok) {
            console.log("typedef undefined....")
            return;
          }
          to = ok
          //ADDING Node
          dialogs.prompt('Transition label:', function(ok) {

            if (!ok) {
              console.log("typedef undefined....")
              return;
            }
            label = ok
            try {
              edges.add({
                id: edgeId,
                from: from,
                to: to,
                label: label
              })
              edgeId++;
            } catch (err) {
              alert(err);
            }

          })
        })
      })

    };

    button_add_state.onclick = function() {
      console.log("tring to create state...");
      dialogs.prompt('Enter node ID:', function(ok) {
        if (!ok) {
          console.log("typedef undefined....")
          return;
        }
        id = ok
        // console.log('ID:', ok)
        dialogs.prompt('Enter node label:', function(ok) {
          if (!ok) {
            console.log("typedef undefined....")
            return;
          }
          label = ok
          console.log('Label:', ok)
          dialogs.prompt('Enter node name:', function(ok) {
            if (!ok) {
              console.log("typedef undefined....")
              return;
            }
            name = ok
            console.log('name:', ok)
          //ADDING Node
          try {
            nodes.add({
              id: id,
              label: label,
              name: name
            });
            console.log(id);
          } catch (err) {
            alert(err);
          }

        })
      })
      })
    };

    button_remove_edge.onclick = function() {
      console.log("In button remove node")
      dialogs.prompt('Remove Transition id:', function(ok) {
        if (!ok) {
          console.log("typedef undefined....")
          return;
        }
        console.log("OK value: " + ok)
        try {
          edges.remove({
            id: ok
          });
        } catch (err) {
          alert(err);
        }
      })
    };
    button_remove_node.onclick = function() {
      dialogs.prompt('Remove State ID:', function(ok) {
        if (!ok) {
          console.log("typedef undefined....")
          return;
        }
        label = ok
        var items = edges.get({
          fields: ['from', 'to', 'name', 'id'] // output the specified fields only
        })
        console.log("items: " + items)
        for (i = 0; i < items.length; i++) {
          //TEST FROM
          console.log("from: " + items[i].from + " to " + items[i].to)
          if (items[i].from == ok || items[i].to == ok) {
            //remove that transition
            try {
              edges.remove({
                id: items[i].id
              });
              console.log("removed node " + items[i].id)
            } catch (err) {
              alert(err);
            }

          }
        }
        try {
          nodes.remove({
            id: ok
          });
        } catch (err) {
          alert(err);
        }
      })
    }

    button_generate_rol.onclick = function() {
      var items = edges.get({
        fields: ['from', 'to', 'name'] // output the specified fields only
      });

      var i;
      var result = "node(" + '\n' + '  name:"myFSM",' + "\n" + "  initialise(" + '\n' + "    FiniteStateMachine<{" + '\n';
      for (i = 0; i < items.length; i++) {
        result += "        " + items[i].from + "-(" + items[i].name + ')->' + items[i].to + '\n';
      }
      result += "    }>" + '\n' + "  )" + '\n' + ')';
      const editor = atom.workspace.getActiveTextEditor()
      if (editor) {
        editor.insertText(result)
      }
    }

    // the finite state machine graphics
    p_element = document.createElement('p')
    vis_element = document.createElement('div')
    edges_label = document.createElement('label')
    nodes_label = document.createElement('label')
    edges_div = document.createElement('pre')
    nodes_div = document.createElement('pre')
    vis_element.setAttribute('id', 'visualization')

    p_element.innerHTML = "ROL FiniteStateMachine studio"
    edges_label.innerHTML = "Transitions"
    nodes_label.innerHTML = "States"
    // join everything
    main_element.appendChild(p_element)
    main_element.appendChild(button_view)
    main_element.appendChild(button_add_state)
    main_element.appendChild(button_remove_node)
    main_element.appendChild(button_add_arc)
    main_element.appendChild(button_remove_edge)
    main_element.appendChild(button_generate_rol)
    main_element.appendChild(vis_element)
    main_element.appendChild(edges_label)
    main_element.appendChild(edges_div)
    main_element.appendChild(nodes_label)
    main_element.appendChild(nodes_div)


    nodes_div.innerHTML = JSON.stringify(nodes.get(), null, 4);
    edges_div.innerHTML = JSON.stringify(edges.get(), null, 4);

    nodes.on('*', function() {
      nodes_div.innerHTML = JSON.stringify(nodes.get(), null, 4);
    });
    edges.on('*', function() {
      edges_div.innerHTML = JSON.stringify(edges.get(), null, 4);
    });
    // create decoration
    editor = atom.workspace.getActiveTextEditor()
    marker = editor.markScreenPosition(editor.getCursorBufferPosition())
    editor.decorateMarker(marker, {
      type: 'block',
      position: 'before',
      item: main_element,
      size: '1000'
    })

  },





}
