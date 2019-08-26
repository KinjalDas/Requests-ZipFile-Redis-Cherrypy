$(document).ready(function() {

        $('#search-table').css("display", "none");

        $.ajax({
        type: 'GET',
        url: 'http://ec2-18-220-250-1.us-east-2.compute.amazonaws.com/generator',
        dataType: 'json',
        success: function(data) {
            var rows = [];
            $.each(data,function(index,value) {
                rows.push('<tr><td>'+value['code']+'</td><td>'+value['name']+'</td><td>'+value['open']+'</td><td>'+value['high']+'</td><td>'+value['low']+'</td><td>'+value['close']+'</td></tr>');
            });
            console.log(rows.join(''));
            $('#record-table').append(rows.join(''));
          }
        });

        $("#search-button").click(function(e) {
          $("#search-table > tbody").empty();
          $.ajax({
            type: 'POST',
            url: 'http://ec2-18-220-250-1.us-east-2.compute.amazonaws.com/generator',
            data: {"search_string": $("#search-text").val().toUpperCase()},
            dataType: 'json',
            success: function(data) {
            var rows = [];
            $.each(data,function(index,value) {
                rows.push('<tr><td>'+value['code']+'</td><td>'+value['name']+'</td><td>'+value['open']+'</td><td>'+value['high']+'</td><td>'+value['low']+'</td><td>'+value['close']+'</td></tr>');
            });
            console.log(rows.join(''));
            $('#search-table').append(rows.join(''));
            $('#search-table').css("display", "");
          }
          })
        });
      });