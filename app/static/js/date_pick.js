$(function () {
    now_date = new Date();
    now_date.setMinutes(0);
    now_date.setHours(now_date.getHours()+1);
    $('#datetime').daterangepicker({
        singleDatePicker: true,
        autoUpdateInput: false,
        minDate: moment(now_date).format('DD.MM.YYYY HH:mm'),
        showDropdowns: true,
        timePicker: true,
        timePicker24Hour:true,
        locale: {
            format: 'DD.MM.YYYY HH:mm'
        }
    })

  $('#datetime').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('DD.MM.YYYY HH:mm'));
  });

  $('#datetime').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
});