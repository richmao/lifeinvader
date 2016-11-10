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

    function get_posts_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return posts_url + "?" + $.param(pp);
    }

    self.get_posts = function () {
        $.getJSON(get_posts_url(0, 4), function (data) {
            self.vue.posts = data.posts;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        })
    };

    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(num_posts, num_posts + 4), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.posts, data.posts);
        });
    };

    self.add_post_button = function () {
        // The button to add a post has been pressed.
        self.vue.is_adding_post = !self.vue.is_adding_post;
    };

    self.edit_post_button = function (post_id) {
        // The button to edit a post has been pressed.
        self.vue.is_editing_post = true;
        self.vue.editing_id = post_id;
    };

    self.add_post = function () {
        // The submit button to add a post has been added.
        $.post(add_post_url,
            {
                post_content: self.vue.form_content,
            },
            function (data) {
                $.web2py.enableElement($("#post-button"));
                self.vue.posts.unshift(data.post);
            });
        self.vue.form_content = "";
        //location.reload();
    };

    self.del_post = function (post_id) {
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

    self.edit_post = function(post_id, edit_content)  {
      $.post(edit_post_url,
            {
                post_id: post_id,
                post_content: edit_content
            },
            function (data) {
                $.web2py.enableElement($("#update-button"));
                for(var i = 0; i < self.vue.posts.length; i++) {
                    if(self.vue.posts[i].id == post_id) {
                         self.vue.posts[i].updated_on = data.updated_on;
                    }
                }
            });
        //location.reload();
    };

    self.convert_time = function(pytime)    {
            t = new Date(pytime);
            return t.toLocaleString();
    }

    self.is_author = function(user) {
        return current_user === user;
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            is_adding_post: false,
            is_editing_post: false,
            posts: [],
            has_more: false,
            logged_in: false,
            form_content: null,
            editing_id: null,
        },
        methods: {
            get_more: self.get_more,
            add_post_button: self.add_post_button,
            edit_post_button: self.edit_post_button,
            add_post: self.add_post,
            del_post: self.del_post,
            edit_post: self.edit_post,
            convert_time: self.convert_time,
            is_author: self.is_author
        }

    });

    self.get_posts();
    $("#vue-div").show();


    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
