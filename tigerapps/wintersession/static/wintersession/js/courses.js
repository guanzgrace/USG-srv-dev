window.App = Ember.Application.create();
App.ApplicationAdapter = DS.FixtureAdapter;

App.Router.map(function() {
    this.resource('courses', { path: '/' });
});


App.Course = DS.Model.extend({
    title: DS.attr('string'),
    description: DS.attr('string'),
    min_enroll: DS.attr('number'),
    max_enroll: DS.attr('number'),
    sections: DS.hasMany('sections')
});

App.Section = DS.Model.extend({
    course: DS.belongsTo('course'),
    blocks: DS.attr('object')
});

App.Registration = DS.Model.extend({
    course: DS.belongsTo('course')
});
