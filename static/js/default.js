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

    self.get_more = function () {
        var num_posts = self.vue.posts.length;
        $.getJSON(get_posts_url(num_posts, num_posts + 4), function (data) {
            self.vue.has_more = data.has_more;
            self.extend(self.vue.posts, data.posts);
        });
    };

    self.like_image = function(image_id)  {
        $.post(like_image_url,
            {
                image_id: image_id,
                username: current_user
            },
            function () {
            });
    };

    self.unlike_image = function(image_id)  {
        $.post(unlike_image_url,
            {
                image_id: image_id,
                username: current_user
            },
            function () {
            });
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            has_more: false,
            logged_in: false,
        },
        methods: {
            like_image: self.like_image,
            get_images: self.get_images,
            unlike_image: self.unlike_image
        }

    });

    //self.get_images();
    $("#vue-div").show();


    return self;
};

function toggleLike(id)
{
    console.log("toggle" + id);
    var e = document.getElementById(id);
    if (e.style.display == 'block' || e.style.display=='')
    {
        e.style.display = 'none';
    }
    else
    {
        e.style.display = 'block';
    }
}
var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
