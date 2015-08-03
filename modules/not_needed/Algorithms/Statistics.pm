# Author: jkh1
# 2007-02-28

=head1 NAME

  Algorithms::Statistics

=head1 SYNOPSIS



=head1 DESCRIPTION



=head1 CONTACT

 jkh1@sanger.ac.uk

=cut

package Algorithms::Statistics;

use strict;
use Inline ( C =>'DATA',
	     NAME =>'Algorithms::Statistics',
	     DIRECTORY => '/home/www_schn/.inline_dir',
	   );

use Exporter;

our @ISA = ('Exporter');
our @EXPORT = qw(ksprob kstest binomial_coef Poisson Exponential Phypergeom Fishertest shuffle);


=head2 ksprob

 Arg: double
 Description: Kolmogorov-Smirnov probability function
 Returntype: double

=cut

sub ksprob {

  my $alam = shift;
  my $a2 = -2.0*$alam*$alam;
  my $fac=2.0;
  my $sum=0.0;
  my $term;
  my $termbf=0.0;
  for (my $j=1;$j<=100;$j++) {
    $term=$fac*exp($a2*$j*$j);
    $sum += $term;
    return $sum if (abs($term) <= 0.001*$termbf || abs($term) <= 1e-8*$sum);
    $fac = -$fac;
    $termbf=abs($term);
  }
  return 1.0;
}

=head2 kstest

 Arg1: reference to first data set (array)
 Arg2: reference to second data set (array)
 Description: Performs a two-samples Kolmogorov-Smirnov test
 Returntype: array (K-S statistic D and p value)

=cut

sub kstest {

  my ($data1,$data2) = @_;
  my $n1 = scalar(@{$data1});
  my $n2 = scalar(@{$data2});
  @{$data1} = sort {$a<=>$b} @{$data1};
  @{$data2} = sort {$a<=>$b} @{$data2};
  my $en1 = $n1;
  my $en2 = $n2;
  my $d = 0;
  my ($j1,$j2) = (0,0);
  my ($fn1,$fn2) = (0,0);
  while ($j1 < $n1 && $j2 < $n2) {
    my $d1 = ${$data1}[$j1];
    my $d2 = ${$data2}[$j2];
    $fn1 = ($j1++)/$en1 if ($d1 <= $d2);
    $fn2 = ($j2++)/$en2 if ($d2 <= $d1);
    my $dt = abs($fn2-$fn1);
    $d = $dt if ($dt>$d);
  }
  my $en=sqrt($en1*$en2/($en1+$en2));
  my $prob=ksprob(($en+0.12+0.11/$en)*$d);
  return ($d,$prob);
}

=head2 binomial_coef

 Arg1: integer, n
 Arg2: integer, k
 Description: Calculates binomial coefficient (n,k)
 Returntype: double

=cut

sub binomial_coef {

  my ($n,$k) = @_;

  return binco($n,$k);
}

=head2 Poisson

 Arg: double (should be >0)
 Description: Draws a positive integer from a Poisson distribution
 Returntype: integer

=cut

sub Poisson {

  my $m = shift;
  my $x = 0;
  my $t = 0;
  while ($t < $m) {
    $t += Exponential(1);
    $x++;
  }
  return ($x - 1);

}

=head2 Exponential

 Arg: double (should be >0)
 Description: Draws a positive integer from an exponential distribution
 Returntype: integer

=cut

sub Exponential {

  my $m = shift;
  return (-$m * log(1 - rand));

}

=head2 Phypergeom

 Arg1: integer, number of 'good' balls in the urn
 Arg2: integer, number of 'bad' balls in the urn
 Arg3: integer, number of balls picked from the urn
 Arg4: integer, number of 'good' balls picked
 Description: Calculates the probability of i successes in n trials
              from a hypergeometric distribution.
 Returntype: double

=cut

sub Phypergeom {

  # There are M "bad" and N "good" balls in an urn.
  # Pick n of them without replacement. The probability of i successful
  # selection is (M!N!n!(M+N-n)!)/(i!(N-i)!(M+i-n)!(n-i)!(M+N)!)

   my ($N, $M, $n, $i) = @_;

   my $loghyp1 = factln($M)+factln($N)+factln($n)+factln($M+$N-$n);
   my $loghyp2 = factln($i)+factln($N-$i)+factln($M+$i-$n)+factln($n-$i)+factln($M+$N);
   return exp($loghyp1 - $loghyp2);
}

=head2 Fishertest

 Arg: array reference to a 2x2 contingency table
 Description: Calculates the two-sided P-value for Fisher's exact test using
              the minimum-likelihood mid-P value approach.
 Returntype: double

=cut

sub Fishertest {

  my $table = shift;

  my $N = $$table[0][0]+$$table[1][0];
  my $M = $$table[0][1]+$$table[1][1];
  my $n = $$table[0][0]+$$table[0][1];
  my $i = $$table[0][0];

  my @P; # all p-values
  $P[$i] = Phypergeom($N, $M, $n, $i);
  my $sum = 0.5*$P[$i];
  foreach my $j(0..$n) {
    next if ($j == $i || $j>$N || $n-$j>$M);

    $P[$j] = Phypergeom($N, $M, $n, $j);
    if ($P[$j]<$P[$i]) {
      $sum += $P[$j];
    }
    elsif ($P[$j]==$P[$i]) {
      $sum += 0.5*$P[$j];
    }
  }
  return $sum;
}

=head2 shuffle

 Arg: array reference
 Description: Randomly shuffles the array using the Fisher-Yates algorithm.
 Returntype: array reference

=cut

sub shuffle {

  my $array = shift;
  my $i;
  for ($i = @$array; --$i; ) {
    my $j = int rand ($i+1);
    next if $i == $j;
    @$array[$i,$j] = @$array[$j,$i];
  }
  return $array;
}



1;

__DATA__
__C__

double gammln (double xx) {

  double x,tmp,ser;
  static double cof[6]={76.18009172947146,    -86.50532032941677,
			24.01409824083091,    -1.231739572450155,
			0.1208650973866179e-2,-0.5395239384953e-5};
  int j;

  x=xx-1.0;
  tmp=x+5.5;
  tmp -= (x+0.5)*log(tmp);
  ser=1.000000000190015;
  for (j=0;j<=5;j++) {
    x += 1.0;
    ser += cof[j]/x;
  }
  return -tmp+log(2.5066282746310005*ser);
}

double factln(int n) {
  /* calculates ln(n!) */
  double gammln (double xx);
  static double a[101];

  if (n < 0) {
    fprintf(stderr,"ERROR: Negative factorial in factln.\n");
    exit(1);
  }
  if (n <= 1) return 0.0;
  if (n <= 100) return a[n] ? a[n] : (a[n]=gammln(n+1.0));
  else return gammln(n+1.0);

}

double binco (int n, int k) {

  double factln(int n);
  return floor(0.5+exp(factln(n)-factln(k)-factln(n-k)));

}
