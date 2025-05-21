# FROM r-base:4.3.1

# RUN R -e "install.packages(c('Rserve','zoo','syuzhet'), repos='http://cran.rstudio.com/')"

# COPY start_rserve.sh /start_rserve.sh
# RUN chmod +x /start_rserve.sh

# CMD ["/start_rserve.sh"]


FROM r-base:latest

# Install system dependencies needed to compile R packages (especially Rserve)
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages(c('Rserve', 'zoo', 'syuzhet','ggplot2','base64enc'), repos='http://cran.rstudio.com/')"

# Expose Rserve port
EXPOSE 6312

COPY start_rserve.sh /start_rserve.sh
RUN chmod +x /start_rserve.sh

CMD ["/start_rserve.sh"]