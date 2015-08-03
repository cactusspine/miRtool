#Install stuff
#install.packages("amap")
########################
library("amap")
#####taking the parameters of input and output matrix
commandArgs()
in_matrix <- commandArgs()[8]
out_matrix <- commandArgs()[9]
in_matrix
out_matrix
mat = as.matrix(read.table(in_matrix))
reordered = mat[hcluster(mat)$order, hcluster(t(mat))$order]
write.table(reordered, out_matrix, sep = "\t")
proc.time()