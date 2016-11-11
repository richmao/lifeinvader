// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };


    function get_people_url(start_index, end_index) {
        var pp = {
            start_index: start_index,
            end_index: end_index
        };
        return people_url + "?" + $.param(pp);
    }

    self.get_people = function () {
        $.getJSON(get_people_url(0, 10), function (data) {
            self.vue.people = data.people;
            self.vue.has_more = data.has_more;
        });
    };

    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(num_posts, num_posts + 4), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.posts, data.posts);
        });
    };

    self.search_button = function() {
        self.vue.is_searching = !self.vue.is_searching;
        // Removing search_results div if we close the seach window
        if(self.vue.search_results) {
            self.vue.search_results = false;
        }
    };

    self.results_button = function() {
        self.vue.search_results = true;
    };

    self.edit_bio_button = function() {
        self.vue.is_editing_bio = !self.vue.is_editing_bio;
    };

    // THIS IS SUPER BROKEN, clearly doesn't work.
    // Look at the do_search in api.py
    // Right now, the WHOLE user db is being dumped lmao.
    self.do_search = function(form_search_content) {
        $.post(do_search_url,
            {
                form_search_content: form_search_content
            },
            function () {
                $.web2py.enableElement($("#search_submit"));
            }
        );
    };

    self.goto_profile = function(person_username) {
      window.location.href = './profile/' + person_username;
    };

    self.valid_q = function (form_search_content) {
      return form_search_content.length > 0;
    };

    self.add_post = function() {
        $.post(add_post_url,
            {
                post_content: self.vue.form_post_content,
                //author: current_user
            },
            function (data) {
                $.web2py.enableElement($("#add_post_submit"));
                self.vue.posts.unshift(data.post);
            });
        self.vue.form_post_content = "";
        self.vue.is_adding_post = !self.vue.is_adding_post;
    };

    self.my_profile = function() {
        return auth_username === current_profile;
    };

    self.editing_button = function() {
        self.vue.is_editing_post = !self.vue.is_editing_post;
    };

    self.edit_bio = function (auth_username) {
        $.post(edit_post_url,
            {
                auth_username: auth_username
            },
            function () {
                $.web2py.enableElement($("#edit_bio_submit"));
            }
        );
    };

    self.pass = function (post_id) {
      self.vue.edit_id = post_id;
    };

    self.can_edit = function (poster_id) {
      return self.vue.edit_id === poster_id;
    };


    self.delete_post = function (post_id) {
        $.post(del_post_url,
            {
                post_id: post_id
            },
            function () {
                var idx = null;
                for (var i = 0; i < self.vue.posts.length; i++) {
                    if (self.vue.posts[i].id === post_id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.posts.splice(idx - 1, 1);
                }
            }
        )
    };

    self.refresh_page = function () {
        location.reload();
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_searching: false,
            is_editing_bio: false,
            posts: [],
            people: [],
            has_more: false,
            form_search_content: null,
            search_results: false
        },
        methods: {
            get_more: self.get_more,
            get_people: self.get_people,
            search_button: self.search_button,
            results_button: self.results_button,
            edit_bio_button: self.edit_bio_button,
            do_search: self.do_search,
            refresh_page: self.refresh_page,
            goto_profile: self.goto_profile,
            valid_q: self.valid_q,
            my_profile: self.my_profile,
            edit_bio: self.edit_bio
        }

    });

    self.get_people();
    $("#search-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
