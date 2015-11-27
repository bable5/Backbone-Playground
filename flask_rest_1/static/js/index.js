(function () {
var Todos,
    TodosView,
    todosList,
    todosListView,
    templates = {
        task: '<li>{{description}} {{done}}</li>',
    } ;

function api(resource) {
    var fullResource ='/todo/api/v1.0' + resource;
    console.log('full todos: ' + fullResource);
    return fullResource;
}

TodoModel = Backbone.Model.extend({
   defaults : {}
});

TodoCollection = Backbone.Collection.extend({
    url: api('/tasks'),
    model: TodoModel,

    parse: function(data) {
        console.log("parsing");
        console.log(data);
        return data.tasks;
    }
});

TodosView = Backbone.View.extend({
    el: '#todo-list',

    initialize: function (options) {
        var self = this;
        _.extend(this.collection, options.collection);
        this.collection.fetch({
            success: function () { self.render(); }
        });
    },

    render: function () {
        var html = '',
            list = '';
        function renderItem(item) {
            return Mustache.to_html(templates.task, {
                description: item.get('description'),
                done: item.get('done')
            });
        }
        console.log('Render the todos');
        console.log(this.collection);

        this.collection.each(function (item) {
            list = list + renderItem(item);
        });
        html = '<ul id="todo-list">' + list + '</ul>';
        console.log(html);
        this.$el.html(html);
        return this;
    }
});

todosList = new TodoCollection();

todosListView = new TodosView({collection: todosList});
todosListView.render();

}());


