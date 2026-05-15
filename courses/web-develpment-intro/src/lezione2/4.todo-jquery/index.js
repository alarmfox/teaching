// Utilizziamo la sintassi jQuery $(selector)
$(document).ready(function() {
    let tasks = JSON.parse(localStorage.getItem('jqueryTasks')) || [];

    function saveAndRender() {
        localStorage.setItem('jqueryTasks', JSON.stringify(tasks));
        render();
    }

    function render() {
        const $list = $('#todoList');
        $list.empty(); // Equivalente a innerHTML = ''

        tasks.forEach((task, index) => {
            // Creiamo l'elemento con la sintassi fluida di jQuery
            const $li = $('<li>')
                .text(task.text)
                .toggleClass('completed', task.completed)
                .append($('<span>').text('X').addClass('delete-btn').click(function(e) {
                    e.stopPropagation(); // Evitiamo che il click attivi anche il toggle
                    tasks.splice(index, 1);
                    saveAndRender();
                }))
                .click(function() {
                    tasks[index].completed = !tasks[index].completed;
                    saveAndRender();
                });
            
            $list.append($li);
        });
    }

    $('#addBtn').click(function() {
        const text = $('#todoInput').val().trim();
        if (text) {
            tasks.push({ text: text, completed: false });
            $('#todoInput').val('');
            saveAndRender();
        }
    });

    // Supporto per il tasto Enter
    $('#todoInput').keypress(function(e) {
        if(e.which == 13) $('#addBtn').click();
    });

    render();
});
