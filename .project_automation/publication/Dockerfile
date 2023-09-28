FROM public.ecr.aws/codebuild/amazonlinux2-x86_64-standard:4.0
RUN yum install -y yum-utils && yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && yum install -y gh 
RUN pip install --upgrade taskcat

# https://github.com/gohugoio/hugo/releases
ENV HUGO_VERSION=0.111.3

RUN yum install -y yum-utils && \
    yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
    yum install -y gh && \
    pip3 install --upgrade pip && \
    go env -w GOPROXY=direct && \
    pushd /tmp && \
    wget -q -nv https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_linux-amd64.tar.gz && \
    tar -xzf hugo_${HUGO_VERSION}_linux-amd64.tar.gz && \
    mv ./hugo /usr/bin/ && \
    popd && \
    gem install asciidoctor
