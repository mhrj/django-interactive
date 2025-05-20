# r_app/start_rserve.R
library(Rserve)
Rserve(args="--RS-port 6312 --vanilla --RS-enable-remote")

