function deleteNote(noteId){
    $.ajax({
        type: "DELETE",
        url: 'http://127.0.0.1:5000/note/'+noteId,
        data: {},
        success: function(response){delete_element(response.data.id);},
        dataType: 'JSON'
      });
}

function delete_element(id){
    $('#'+id).remove()
}

function toggleModal(){
    $('#myModal').modal("toggle");
}