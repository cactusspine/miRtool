#!/usr/bin/perl -w

#use DbGpcr;
use DbGprotein;

use strict;

	my $level = "class";
	my $node = "Galpha";
	my $sort_by_field_name = "name";
	my $asc_or_desc = "asc";
	my @geneProteinIds = &DbGprotein::GetIds($level, $node, $sort_by_field_name, $asc_or_desc);

print "geneProteinIds : @geneProteinIds";
