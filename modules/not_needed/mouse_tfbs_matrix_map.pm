package mouse_tfbs_matrix_map;

sub get_matrix_id { 
  my $matrix_name = shift; 
	my %matrix_name_id_hash = ( 
'Arnt' => 'MA0004',
'Arnt-Ahr' => 'MA0006',
'T' => 'MA0009',
'Pax5' => 'MA0014',
'En1' => 'MA0027',
'Evi1' => 'MA0029',
'Gata1' => 'MA0035',
'Klf4' => 'MA0039',
'Nkx2-5' => 'MA0063',
'Pax2' => 'MA0067',
'Pax4' => 'MA0068',
'Prrx2' => 'MA0075',
'Sox17' => 'MA0078',
'Sox5' => 'MA0087',
'Hand1-Tcfe2a' => 'MA0092',
'Fos' => 'MA0099',
'Myb' => 'MA0100',
'Mycn' => 'MA0104',
'Spz1' => 'MA0111',
'Bapx1' => 'MA0122',
'Nobox' => 'MA0125',
'Pdx1' => 'MA0132',
'Lhx3' => 'MA0135',
'ELF5' => 'MA0136'
);

my $matrix_id = $matrix_name_id_hash{$matrix_name}; 
return $matrix_id; 
} # sub get_matrix_id {
1;
