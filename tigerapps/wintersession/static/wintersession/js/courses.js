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

App.ApplicationRoute = Ember.Route.extend({
    model: function() {
        this.store.find('course');
        this.store.find('section');
        this.store.find('block');
    }
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
            newReg.save().catch(function(err) {
                alert(err['responseJSON']['registration']['error']);
                newReg.rollback();
                newReg.unloadRecord();
            });
        },
        unregisterSection: function(section) {
            var reg = section.get('registration');
            reg.destroyRecord().catch(function(err) {
                alert(err['responseJSON']['registration']['error']);
                reg.rollback();
            });
        },
        doFilter: function() {
            this.set('filter', this.get('filterValue'));
        }
    },
    filter: '',
    filterValue: '',
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
    }.property('filter', 'courses.@each.title')
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
    sections: DS.hasMany('sections', {async: true}),
    isRegistered: function() {
        var isRegistered = false;
        this.get('sections').forEach(function(section) {
            if (section.get('registration') != null) {
                isRegistered = true;
            }
        });
        return isRegistered;
    }.property('sections.@each.registration')
});

App.Section = DS.Model.extend({
    course: DS.belongsTo('course', {async: true}),
    blocks: DS.hasMany('blocks', {async: true}),
    schedule: DS.attr(),
    schedule_string: DS.attr('string'),
    registration: DS.belongsTo('registration'),
    isRegistered: function() {
        return this.get('registration') != null;
    }.property('registration'),
    isConflicting: function() {
        // Not conflicting if already registered
        if (this.get('isRegistered')) {
            return false;
        }

        // Conflicting if already registered in another section
        if (this.get('course').get('isRegistered')) {
            return true;
        }

        // Check time conflicts
        var isConflicting = false;
        this.get('blocks').forEach(function(block) {
            if (block.get('isRegistered')) {
                isConflicting = true;
            }
        });
        return isConflicting;
    }.property('blocks.@each.isRegistered', 'course.isRegistered')
});

App.Registration = DS.Model.extend({
    section: DS.belongsTo('section', {async: true})
});

App.BlockAdapter = DS.FixtureAdapter;

App.Block = DS.Model.extend({
    sections: DS.hasMany('sections', {async: true}),
    isRegistered: function() {
        var isRegistered = false;
        this.get('sections').forEach(function(section) {
            if (section.get('isRegistered')) {
                isRegistered = true;
            }
        });
        return isRegistered;
    }.property('sections.@each.isRegistered')
});

App.Block.reopenClass({
    FIXTURES: []
});
