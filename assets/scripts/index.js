import 'bootstrap/dist/css/bootstrap.css';
import '../styles/styles.css'
import $ from 'jquery';

// Функція для прокрутки блоку people_worth_following
document.addEventListener("DOMContentLoaded", function() {
    const people_worth_following = document.getElementById("people-worth-following");

    window.addEventListener("scroll", function() {

        if (window.scrollY > 200) {
            people_worth_following.style.position = "fixed";
            people_worth_following.style.top = "10px";
        } else {
            people_worth_following.style.position = "static";
        }
    });
});

// Обробник подій дял кнопок follow\unfollow
$(document).ready(function () {
    $(".follow-button, .unfollow-button").click(function (e) {
        e.preventDefault();

        const button = $(this);
        const user_id = button.data("user-id");
        const action_type = button.data("action-type");
        const csrf_token = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: "POST",
            url: `/follow_or_unfollow/` + user_id,
            data: {
                'action_type': action_type,
            },
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function (data) {
                // Оновлюється кількість підписників\підписок
                $(".followers-count").text(data.followers_count);
                $(".followings-count").text(data.followings_count);

                // Змінюється назви кнопки, в залежності від попереднього стану
                if (action_type === "follow") {
                    button.text("Unfollow").data("action-type", "unfollow").removeClass("btn-primary").addClass("btn-danger");
                } else {
                    button.text("Follow").data("action-type", "follow").removeClass("btn-danger").addClass("btn-primary");
                }
            },
            error: function () {
                console.log('Error');
            }
        });
    });
});

// Обробник подій для кнопок like\dislike
$(document).ready(function() {
    $('.like-button, .dislike-button').click(function(e) {
        e.preventDefault();

        const reaction_type = $(this).data('reaction-type');
        const post_id = $(this).data('post-id');
        const csrf_token = $('[name=csrfmiddlewaretoken]').val();

        $.ajax({
            type: 'POST',
            url: `/reaction/` + post_id,
            data: {
                'reaction_type': reaction_type,
            },
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function(data) {
                // Після виконання певної операції оновлює кількість лайків\дізлайків
                $('.likes-count').text('Likes: ' + data.likes_count);
                $('.dislikes-count').text('Dislikes: ' + data.dislikes_count);
            },
            error: function() {
                console.log('Error');
            },
        });
    });
});
