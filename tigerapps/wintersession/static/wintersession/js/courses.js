window.App = Ember.Application.create({
    rootElement: '#wsite-content'
});

App.ApplicationAdapter = DS.FixtureAdapter;

DS.RESTAdapter.reopen({
    headers: {
        "X-CSRFToken": window.CSRF_TOKEN
    }
});

App.Router.map(function() {
    this.resource('courses', { path: '/' });
});

App.CoursesRoute = Ember.Route.extend({
    model: function() {
        return Ember.RSVP.hash({
            courses: this.store.find('course'),
            registrations: this.store.find('registration')
        });
    }
});

App.CoursesController = Ember.ObjectController.extend({
    actions: {
        registerSection: function(section) {
            var newReg = this.store.createRecord('registration', {
                section: section
            });
            newReg.save().then(null, function() {
                newReg.rollback();
                newReg.unloadRecord();
            });
        }
    },
    filter: '',
    filteredContent: function() {
        var filter = this.get('filter');
        var courses = this.get('courses');
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
    }.property('filter', 'courses')
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
    schedule_string: DS.attr('string'),
    registration: DS.belongsTo('registration')
});

App.Registration = DS.Model.extend({
    section: DS.belongsTo('section', {async: true})
});
