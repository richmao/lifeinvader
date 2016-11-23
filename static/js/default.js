// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false;
    Vue.config.devtools = true;
    // show all warnings


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


    function get_images_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return images_url + "?" + $.param(pp);
    }

    self.get_images = function () {
        $.getJSON(get_images_url(0, 4), function (data) {
            self.vue.images = data.images;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        })
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


    self.goto_profile = function(person_username) {
      window.location.href = '/default/profile/' + person_username;
    };

    self.valid_q = function (form_search_content) {
      return form_search_content.length > 0;
    };


    self.my_profile = function() {
        return current_user === current_profile;
    };

    self.editing_button = function() {
        self.vue.is_editing_post = !self.vue.is_editing_post;
    };

    self.pass = function (post_id) {
      self.vue.edit_id = post_id;
    };


    self.refresh_page = function () {
        location.reload();
    };

    self.toggle_like = function (image_id) {
        $.post(toggle_like_url,
            {
                image_id: image_id,
                username: current_user
            },
            function () {
            }
        );
    };

    self.toggle_follow = function () {
        $.post(toggle_follow_url,
            {
                add_user: current_user,
                username: current_profile
            },
            function () {
                if(self.vue.is_following == 1){
                    self.vue.is_following = 0;
                } else {
                    self.vue.is_following = 1;
                }
            }
        );
    };

    self.add_comment_button = function (image_id) {
        // The button to edit a post has been pressed.
        self.vue.is_adding_comment = !self.vue.is_adding_comment;
        self.vue.adding_id = image_id;
    };

    self.add_comment = function (comment_content, image_id)  {
        $.post(add_comment_url,
            {
                comment_content: comment_content,
                image_id: image_id
            },
            function (data) {
                $.web2py.enableElement($("#add_comment_submit"));
                // push is the opposite of unshift, should post
                // comment at end of array.
                self.vue.comments.push(data.comment);

            }
        );
        self.vue.form_comment_content = "";
    };

    self.get_comments = function() {
        $.getJSON(get_comments_url, function (data) {
            self.vue.comments = data.comments;
        });
    };

    self.toggle = function() {
        self.vue.upload = !self.vue.upload;
    };


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_searching: false,
            is_editing_bio: false,
            is_following: parseInt(p_is_following),
            is_adding_comment: false,
            people: [],
            comments: [],
            has_more: false,
            form_search_content: null,
            search_results: false,
            follower_count: parseInt(f_count),
            adding_id: null,
            form_comment_content: null,
            upload: true
        },
        methods: {
            get_people: self.get_people,
            search_button: self.search_button,
            results_button: self.results_button,
            refresh_page: self.refresh_page,
            goto_profile: self.goto_profile,
            valid_q: self.valid_q,
            my_profile: self.my_profile,
            toggle_like: self.toggle_like,
            toggle_follow: self.toggle_follow,
            add_comment: self.add_comment,
            add_comment_button: self.add_comment_button,
            toggle: self.toggle
        }

    });




    self.get_people();
    self.get_comments();
    //self.get_images();
    //$("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
