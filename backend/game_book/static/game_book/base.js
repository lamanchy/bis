const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const a = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

add_icon = (el, name) => {
    el.classList.remove("spinner-border")
    el.classList.remove("spinner-border-sm")
    el.classList.add(`bi`)
    el.classList.add(`bi-${name}`)
}
remove_icon = (el, name) => {
    el.classList.add("spinner-border")
    el.classList.add("spinner-border-sm")
    el.classList.remove(`bi`)
    el.classList.remove(`bi-${name}`)
    el.classList.remove(`bi-${name}-fill`)
}
state_to_icon = {
    favourites: 'star',
    is_verified: 'patch-check',
    thumbs_up: 'hand-thumbs-up',
    watchers: 'eye',
}

function toggle_state(event, el, game_id, state) {
    event.stopPropagation()
    el = el.children[0]
    let icon = state_to_icon[state]
    remove_icon(el, icon)

    axios
        .post(`/game_book/game/${game_id}/toggle/${state}/`, {}, {headers: {'X-CSRFToken': CSRF_TOKEN}})
        .then(({data}) => add_icon(el, icon + (data.on ? '-fill' : '')))
        .catch((error) => add_icon(el, "exclamation-lg"))
}
