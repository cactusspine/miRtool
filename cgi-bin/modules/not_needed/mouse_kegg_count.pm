package mouse_kegg_count;

sub get_kegg_count {
my $kegg_pathway_id = shift;

my %mouse_kegg_count = (
'mmu00010' => 129,
'mmu00020' => 43,
'mmu00030' => 34,
'mmu00040' => 34,
'mmu00051' => 41,
'mmu00052' => 32,
'mmu00053' => 29,
'mmu00061' => 12,
'mmu00062' => 9,
'mmu00071' => 58,
'mmu00072' => 17,
'mmu00100' => 20,
'mmu00120' => 16,
'mmu00130' => 11,
'mmu00140' => 57,
'mmu00190' => 262,
'mmu00230' => 184,
'mmu00232' => 12,
'mmu00240' => 110,
'mmu00250' => 50,
'mmu00260' => 49,
'mmu00270' => 45,
'mmu00280' => 56,
'mmu00290' => 14,
'mmu00300' => 8,
'mmu00310' => 47,
'mmu00330' => 64,
'mmu00340' => 28,
'mmu00350' => 42,
'mmu00360' => 25,
'mmu00380' => 44,
'mmu00400' => 14,
'mmu00410' => 30,
'mmu00430' => 15,
'mmu00450' => 26,
'mmu00460' => 15,
'mmu00471' => 6,
'mmu00472' => 2,
'mmu00480' => 59,
'mmu00500' => 51,
'mmu00510' => 52,
'mmu00511' => 18,
'mmu00512' => 29,
'mmu00514' => 3,
'mmu00520' => 51,
'mmu00524' => 6,
'mmu00531' => 27,
'mmu00532' => 27,
'mmu00533' => 18,
'mmu00534' => 33,
'mmu00561' => 56,
'mmu00562' => 58,
'mmu00563' => 28,
'mmu00564' => 86,
'mmu00565' => 36,
'mmu00590' => 91,
'mmu00591' => 46,
'mmu00592' => 18,
'mmu00600' => 47,
'mmu00601' => 34,
'mmu00603' => 15,
'mmu00604' => 21,
'mmu00620' => 55,
'mmu00630' => 26,
'mmu00640' => 39,
'mmu00650' => 46,
'mmu00670' => 21,
'mmu00680' => 14,
'mmu00730' => 13,
'mmu00740' => 18,
'mmu00750' => 10,
'mmu00760' => 29,
'mmu00770' => 20,
'mmu00780' => 3,
'mmu00785' => 5,
'mmu00790' => 14,
'mmu00830' => 89,
'mmu00860' => 42,
'mmu00900' => 21,
'mmu00903' => 12,
'mmu00910' => 28,
'mmu00920' => 13,
'mmu00970' => 55,
'mmu00980' => 79,
'mmu00982' => 87,
'mmu00983' => 58,
'mmu01040' => 28,
#'mmu01100' => 1387,
'mmu02010' => 45,
'mmu03010' => 132,
'mmu03018' => 73,
'mmu03020' => 35,
'mmu03022' => 36,
'mmu03030' => 36,
'mmu03040' => 152,
'mmu03050' => 51,
'mmu03060' => 37,
'mmu03320' => 95,
'mmu03410' => 56,
'mmu03420' => 47,
'mmu03430' => 25,
'mmu03440' => 28,
'mmu03450' => 14,
'mmu04010' => 285,
'mmu04012' => 101,
'mmu04020' => 209,
'mmu04060' => 252,
'mmu04062' => 209,
'mmu04070' => 81,
'mmu04080' => 291,
'mmu04110' => 154,
'mmu04114' => 132,
'mmu04115' => 78,
'mmu04120' => 153,
'mmu04130' => 39,
'mmu04140' => 42,
'mmu04142' => 133,
'mmu04144' => 222,
'mmu04146' => 90,
'mmu04150' => 60,
'mmu04210' => 99,
'mmu04260' => 97,
'mmu04270' => 136,
'mmu04310' => 172,
'mmu04320' => 22,
'mmu04330' => 59,
'mmu04340' => 58,
'mmu04350' => 97,
'mmu04360' => 142,
'mmu04370' => 85,
'mmu04510' => 215,
'mmu04512' => 85,
'mmu04514' => 173,
'mmu04520' => 87,
'mmu04530' => 147,
'mmu04540' => 101,
'mmu04610' => 77,
'mmu04612' => 109,
'mmu04614' => 21,
'mmu04620' => 112,
'mmu04621' => 69,
'mmu04622' => 74,
'mmu04623' => 60,
'mmu04630' => 165,
'mmu04640' => 86,
'mmu04650' => 138,
'mmu04660' => 137,
'mmu04662' => 90,
'mmu04664' => 88,
'mmu04666' => 109,
'mmu04670' => 124,
'mmu04672' => 62,
'mmu04710' => 14,
'mmu04720' => 84,
'mmu04722' => 150,
'mmu04730' => 80,
'mmu04740' => 983,
'mmu04742' => 61,
'mmu04810' => 230,
'mmu04910' => 152,
'mmu04912' => 108,
'mmu04914' => 93,
'mmu04916' => 112,
'mmu04920' => 72,
'mmu04930' => 54,
'mmu04940' => 77,
'mmu04950' => 28,
'mmu04960' => 48,
'mmu04962' => 47,
'mmu04964' => 24,
'mmu05010' => 287,
'mmu05012' => 189,
'mmu05014' => 74,
'mmu05016' => 247,
'mmu05020' => 45,
'mmu05140' => 75,
'mmu05200' => 376,
'mmu05210' => 81,
'mmu05211' => 80,
'mmu05212' => 84,
'mmu05213' => 64,
'mmu05214' => 82,
'mmu05215' => 99,
'mmu05216' => 36,
'mmu05217' => 62,
'mmu05218' => 84,
'mmu05219' => 51,
'mmu05220' => 90,
'mmu05221' => 70,
'mmu05222' => 99,
'mmu05223' => 65,
'mmu05310' => 42,
'mmu05320' => 91,
'mmu05322' => 192,
'mmu05330' => 77,
'mmu05332' => 77,
'mmu05340' => 41,
'mmu05410' => 90,
'mmu05412' => 80,
'mmu05414' => 99,
'mmu05416' => 119,
);

my $count = $mouse_kegg_count{$kegg_pathway_id};
return $count;
} # get_kegg_count{
1;
