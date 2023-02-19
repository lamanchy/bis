
let filter_panel = $('#filterPanel')
$('#id_administration_unit').select2({
    theme: 'bootstrap-5',
    dropdownParent: filter_panel,
})

$('#id_contributor').select2({
    theme: 'bootstrap-5',
    dropdownParent: filter_panel,
})

function handle_quick_search_button_submit(params) {
    event.preventDefault()
    let searchParams = new URLSearchParams()
    Object.entries(params).forEach(([key, value]) => searchParams.set(key, value))
    window.location.search = searchParams.toString()
}

function handle_quick_search_form_submit(form, event) {
    event.preventDefault()
    let searchParams = new URLSearchParams(window.location.search)
    searchParams.set("search_input", form.querySelector("#search_input").value)
    searchParams.set("order", form.querySelector("#order").value)
    window.location.search = searchParams.toString()
}
