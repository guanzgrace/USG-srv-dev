window.App = Ember.Application.create({
    rootElement: '#wsite-content'
});
App.ApplicationAdapter = DS.FixtureAdapter;

App.Router.map(function() {
    this.resource('courses', { path: '/' });
});

App.CoursesRoute = Ember.Route.extend({
    model: function() {
        return this.store.find('course');
    }
});

App.CoursesController = Ember.ArrayController.extend({
    filter: '',
    filteredContent: function() {
        var filter = this.get('filter');
        var courses = this.get('arrangedContent');
        if (filter == '') {
            return courses;
        } else {
            var search = new BitapSearcher(filter);
            return courses.filter(function(course) {
                var result = search.search(course.get('title'));
                course.set('score', result.score);
                return result.isMatch;
            }).sort(function(a, b) {
                return a.get('score') - b.get('score');
            });
        }
    }.property('filter', 'arrangedContent')
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
    sections: DS.hasMany('sections', {async: true})
});

App.Section = DS.Model.extend({
    course: DS.belongsTo('course', {async: true}),
    blocks: DS.attr(),
    schedule: DS.attr(),
    schedule_string: DS.attr('string')
});

App.Registration = DS.Model.extend({
    section: DS.belongsTo('section', {async: true})
});
