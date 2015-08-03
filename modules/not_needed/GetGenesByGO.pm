#!/usr/local/bin/perl -w

# Author: jkh1
# 2009-10-22

# Given a GO term and a list of genes, extract genes from the list that are
# annotated with the given term or any of its children.

# Uses a GO terms database and a file of gene annotations

package GetGenesByGO;

use strict;
use DBI;

our @ISA = ('Exporter');
our @EXPORT = qw(get_genes_by_GO);


# GO terms database
my $dsn="DBI:mysql:dbname=mygo;host=10.11.8.30";
my $goh= DBI->connect ($dsn, 'sudo_all','m1SRKmug', {RaiseError=> 1, PrintError=> 0});

## Get this file with BioMart
#my $go_annotations = "$ENV{'HOME'}/Data/GO/Ensembl_v53_annotations.txt";

sub get_genes_by_GO {

  # $GOID: ID of GO term for which we want genes
  # $list: List ref of Ensembl gene IDs from which to extract genes annotated with the selected term or any of its children
  my ($GOID,$list,$org) = @_;

	my $go_dir = "/usr/local/www_schn/apache22/cgi-bin/biocompendium_perl/GO/";
 	my $gene_annotations_file = ""; 

 if($org eq "human") {
    $gene_annotations_file = $go_dir . "human_annotations.txt";
  }
  elsif($org eq "mouse") {
    $gene_annotations_file = $go_dir . "mouse_annotations.txt";
  }
  elsif($org eq "yeast") {
    $gene_annotations_file = $go_dir . "yeast_annotations.txt";
  }

  # Read all GO annotations into memory from file
  # (faster than using Ensembl database)
  my %go2genes;
  open FH,"<",$go_annotations or die "Can't read file $go_annotations: $!\n";
  while (my $line = <FH>) {
    chomp($line);
    my ($geneID,$goacc) = split(/\t/,$line);
    next unless $goacc;
    push @{$go2genes{$goacc}},$geneID;
  }
  close FH;

  # Get all genes annotated with this term and its children
  my @genes;
  if ($go2genes{$GOID}) {
    @genes = @{$go2genes{$GOID}};
  }
  my @q = &get_all_child_terms($GOID);
  foreach my $ac(@q) {
    push @genes,@{$go2genes{$ac}} if ($go2genes{$ac});
  }
  my %seen;
  @genes = grep {!$seen{$_}++} @genes; # remove duplicates

  # Limit to the genes under consideration
  my %is_query;
  foreach my $geneID(@{$list}) {
    $is_query{$geneID}++;
  }
  @genes = grep {$is_query{$_}} @genes;

 return @genes;

}

sub get_all_child_terms {

  my $acc = shift;
  my @children;
  my $child_query = qq(SELECT DISTINCT child.acc
                       FROM term as ancestor, graph_path, term as child
                       WHERE ancestor.id=graph_path.term1_id
                       AND child.id=graph_path.term2_id
                       AND graph_path.distance>0
                       AND ancestor.acc= ?);
  my $gosth = $goh->prepare($child_query);
  $gosth->execute($acc);
  while (my ($child) = $gosth->fetchrow_array()) {
    push @children,$child;
  }
  return @children;
}

1;
