window.App = Ember.Application.create();
App.ApplicationAdapter = DS.FixtureAdapter;

App.Router.map(function() {
    this.resource('courses', { path: '/' });
});

App.CoursesRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('course');
    }
});

App.ApplicationAdapter = DS.RESTAdapter.extend({
    namespace: 'api'
});

App.Course = DS.Model.extend({
    title: DS.attr('string'),
    description: DS.attr('string'),
    min_enroll: DS.attr('number'),
    max_enroll: DS.attr('number'),
    cancelled: DS.attr('boolean'),
    room: DS.attr('string'),
    instructors: DS.attr(),
    sections: DS.hasMany('sections')
});

App.Section = DS.Model.extend({
    course: DS.belongsTo('course'),
    blocks: DS.attr(),
    schedule: DS.attr()
});

App.Registration = DS.Model.extend({
    section: DS.belongsTo('section')
});
