const sort = (url) => {
    const sortDirections = document.getElementById("sort-direction");
    const sortFields = document.getElementById("sort-field");
    const sortButton = document.getElementById("btn-sort");
    let sortDirection = sortDirections.value;
    let sortField = sortFields.value;

    window.addEventListener("DOMContentLoaded", ()=> {
        sortDirections.addEventListener("change", () =>
        {
            sortDirection = sortDirections.value;
        })
        sortFields.addEventListener("change", () => {
            sortField = sortFields.value;
        })
        sortButton.addEventListener("click", ()=>{
            window.location.replace(url+"?sort_field=" + sortField + "&sort_direction=" + sortDirection);
        });
    })
}