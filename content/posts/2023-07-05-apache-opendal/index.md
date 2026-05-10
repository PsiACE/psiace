+++
title = "Apache OpenDAL (Incubating): A Painless New Data Access Experience"
description = "An introduction to Apache OpenDAL's positioning, strengths, use cases, and roadmap."
date = 2023-07-05
slug = "apache-opendal"

[taxonomies]
tags = ["2023", "ASF", "OpenDAL"]

[extra]
lang = "en"
+++

> This article is mainly organized from [An Introduction for Java Users | @Xuanwo](https://note.xuanwo.io/#/page/opendal%2F%E9%9D%A2%E5%90%91%20java%20%E7%94%A8%E6%88%B7%E7%9A%84%E4%BB%8B%E7%BB%8D).

If you are committed to building cloud-native, cloud-agnostic applications and services, or you want to support configurable storage backends for complex data access needs, or you are tired of juggling different SDKs and expect a unified abstraction and developer experience, Apache OpenDAL (Incubating) will be an excellent partner.

![Apache OpenDAL (Incubating) Arch](apache-opendal.png)

## What Is OpenDAL?

OpenDAL is a data access layer that allows users to retrieve data from various storage services easily and efficiently in a unified way.

**Data access layer** means that OpenDAL sits at a key position between the upper and lower parts of the data read/write flow. We hide implementation details of different storage backends and provide a unified interface abstraction externally.

Next, let us try to answer "what OpenDAL is not" and deconstruct OpenDAL from another angle.

### OpenDAL Is Not a Proxy Service

OpenDAL is provided as a library, not as a service or application that proxies various storage backends.

If you want to integrate OpenDAL into an existing project, you need to call OpenDAL APIs through a supported language and directly access the storage service.

### OpenDAL Is Not an SDK Aggregator

Although OpenDAL replaces the position of various SDKs in application architecture, it is not implemented as an SDK aggregator.

In other words, OpenDAL does not simply call SDKs from different storage services. Based on a unified Rust core, we implement integrations with storage services ourselves to smooth over differences between services.

Taking S3 as an example, OpenDAL manually constructs HTTP requests and parses HTTP responses, ensuring that all behavior conforms to the API specification and remains fully under OpenDAL's control. Because OpenDAL natively takes over the data access flow, we can easily implement unified retry and logging mechanisms for different storage backends and ensure behavioral consistency.

For S3-compatible services, compatibility and behavioral details may still differ from S3 because of limitations in native storage services and API implementation differences. For example, OSS requires a separate header for its default Range behavior to remain consistent. Besides integrating native storage services, OpenDAL also handles compatible services in targeted ways to ensure the user's data access experience.

## Advantages of OpenDAL

OpenDAL is not the only project committed to providing a data access abstraction, but compared with similar projects, OpenDAL has the following advantages.

### Rich Service Support

- OpenDAL supports dozens of storage services, covers a wide range of scenarios, and can be selected as needed:
  - Standard storage protocols: FTP, HTTP, SFTP, WebDAV, and more
  - Object storage services: azblob, gcs, obs, oss, s3, and more
  - File storage services: fs, azdfs, hdfs, webhdfs, ipfs, and more
  - Consumer storage services: Google Drive, OneDrive, Dropbox, and more
  - Key-value storage services: Memory, Redis, Rocksdb, and more
  - Cache services: Ghac, Memcached, and more

### Complete Cross-Language Bindings

- With Rust as the core, OpenDAL now provides bindings for Python, Node.js, Java, C, and other languages, while actively developing bindings for more languages.
- Cross-language bindings not only provide unified storage access abstractions for other languages, but also follow each language's conventional naming style and development habits as much as possible in design and implementation, paving the way for quick adoption.

### Powerful Middleware Support

- OpenDAL provides native middleware capabilities, mainly including:
  - Error retry: OpenDAL supports fine-grained error retry capabilities. Besides common request retries, it supports resuming from breakpoints without rereading the entire file.
  - Observability support: OpenDAL implements logging, tracing, and metrics support for all operations. By enabling middleware, users can directly obtain observability for storage.
  - It also includes concurrency control, traffic control, fuzz testing, and more.

### Simple and Easy to Use

- OpenDAL's API is well designed and continuously polished in real use. Its documentation is comprehensive and makes it easy to get started. The following is an example of using the Python binding to access HDFS:

    ```python
    import opendal

    op = opendal.Operator("hdfs", name_node="hdfs://192.16.8.10.103")
    op.read("path/to/file")
    ```

### OpenDAL Use Cases

OpenDAL is currently widely used in various cloud-native scenarios, including but not limited to databases, data pipelines, and caches. Major user cases include:

- Databend: an OLAP cloud-native data warehouse that uses OpenDAL to read and write persistent data (s3, azblob, gcs, hdfs, and more) and cache data (fs, redis, rocksdb, moka, and more).
- GreptimeDB: a cloud-native time-series database that uses OpenDAL to read and write persistent data (s3, azblob, and more).
- RisingWave: a distributed SQL database for stream processing that uses OpenDAL to read and write persistent data (s3, azblob, hdfs, and more).
- Vector: an observability data pipeline that uses OpenDAL to write persistent data, currently mainly through hdfs.
- Sccache: a ccache-like tool supporting cloud storage, mainly used to cache compilation artifacts for Rust/C++. It uses OpenDAL to read and write cache data such as s3 and ghac.

## OpenDAL's Future Roadmap

Besides further satisfying cloud-native data access needs, OpenDAL will continue expanding user scenarios and actively explore usage in data science, mobile applications, and other areas. OpenDAL will also continue polishing existing implementations and bindings to provide a better integration experience for users.

OpenDAL will also explore how to improve users' workflows in data management and service integration:

- Polish the oli command-line tool to help users manage data painlessly.
- Implement the oay proxy service to provide high-quality compatible APIs.

In addition, because OpenDAL is currently a cross-language project, we also plan to write a series of beginner tutorials to help everyone start from zero and master OpenDAL while learning a language.

## Acknowledgements

- [Apache OpenDAL(Incubating) | Website](https://opendal.apache.org/)
- [apache/incubator-opendal | GitHub](https://github.com/apache/incubator-opendal)
- [An Introduction for Java Users | @Xuanwo](https://note.xuanwo.io/#/page/opendal%2F%E9%9D%A2%E5%90%91%20java%20%E7%94%A8%E6%88%B7%E7%9A%84%E4%BB%8B%E7%BB%8D)
