(function () {
var Todos,
    TodosView,
    todosList,
    todosListView;


function api(resource){
    var fullResource ='/todo/api/v1.0' + resource;
    console.log('full todos: ' + fullResource);
    return fullResource;
}

TodoModel = Backbone.Model.extend({
   defaults : {}
});

TodoCollection = Backbone.Collection.extend({
    url: api('/tasks'),
    model: TodoModel
});

TodosView = Backbone.View.extend({
    el: '#todo-list',

    initialize: function() {
        console.log('Todo view init');
        console.log(this.collection);
    },

    parse: function(data) {
        console.log("parsing");
        console.log(data);
    }

    render: function() {
        console.log('Trying to render');
        debugger;
        var html = '<b>TODO:</b>' + this.model.get('description');
        this.$el.html(html);
        console.log('Render the todos');
        return this;
    }
});

todosList = new TodoCollection();

todosList.fetch().then(function() {
    console.log('fetch the todos');
    console.log(todosList);
});

todosListView = new TodosView({collection: todosList});
todosListView.render();

console.log("TODO COLLECTION");
console.log(todosList);

}());


