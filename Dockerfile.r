FROM r-base:4.3.1

RUN R -e "install.packages('Rserve', repos='http://cran.rstudio.com/')"

COPY start_rserve.sh /start_rserve.sh
RUN chmod +x /start_rserve.sh

CMD ["/start_rserve.sh"]
