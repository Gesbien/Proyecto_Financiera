$(document).ready(function (){
     $('#fabrSel').select2({
        width: 'resolve',
        height: '100%',
        tags: true,
        tokenSeparators: [',', ' '],
        placeholder: 'Selecciona Fabricante',
       selectOnClose: true
    });
     $('#modSel').select2({
        width: 'resolve',
        height: '100%',
        tags: true,
        tokenSeparators: [',', ' '],
        placeholder: 'Selecciona Modelo',
       selectOnClose: true
    });
     var $select1 = $('#fabrSel'),
        $select2 = $('#modSel'),
        $options= $select2.find('option');
        $select1.on('change',function (){
            $select2.html($options.filter('[data-category='+this.value+']'));
        }).trigger('change');
});