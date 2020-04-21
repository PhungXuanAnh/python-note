- [1. Các khái niệm chính](#1-các-khái-niệm-chính)
  - [1.1. triggers](#11-triggers)
  - [1.2. job stores](#12-job-stores)
  - [1.3. Executors](#13-executors)
  - [1.4. Schedulers](#14-schedulers)
- [2. Chọn Scheduler](#2-chọn-scheduler)
- [3. Ví dụ và tham khảo](#3-ví-dụ-và-tham-khảo)

# 1. Các khái niệm chính

## 1.1. triggers

Trigger là logic xác định khi nào 1 job được chạy. Định nghĩa trigger khi thêm job bằng `add_job()` hoặc `scheduled_job()`, tham khảo [add job](https://apscheduler.readthedocs.io/en/stable/userguide.html#adding-jobs)

## 1.2. job stores

Nơi chứa các job được lập lịch. Mặc định là `memory`, nhưng có thể lưu ở một vài loại db.
Job stores chịu trách nhiệm save, load, update, search jobs trong backend
Job stores không chia sẻ giữa các **scheduler**

## 1.3. Executors

Là cái điểu khiển quá trình chạy của job. Cụ thể là submit cái hàm định nghĩa job đến thread or process pool. Khi job done thì **executor** thông báo cho **scheduler** để thằng **scheduler** phát ra một cái sự kiện gì đó.

## 1.4. Schedulers

**Scheduler** gắn các phần còn lại với nhau. App của mình không giao du trực tiếp với mấy thằng **trigger**, **job store**, **executor** mà **scheduler** sẽ cung cấp interface để điều khiển tất cả bọn nó. Như cấu hình job, executor hay thêm, sửa, xóa job. Vậy là khi làm việc với  **apscheduler** ta chỉ quan tâm đến thằng này và các interface mà nó tòi ra cho ta dùng :D


# 2. Chọn Scheduler

Có mấy loại sau [tham khảo](https://apscheduler.readthedocs.io/en/stable/userguide.html#choosing-the-right-scheduler-job-store-s-executor-s-and-trigger-s):

**BlockingScheduler**: use when the scheduler is the only thing running in your process

**BackgroundScheduler**: use when you’re not using any of the frameworks below, and want the scheduler to run in the background inside your application

**AsyncIOScheduler**: use if your application uses the asyncio module

**GeventScheduler**: use if your application uses gevent

**TornadoScheduler**: use if you’re building a Tornado application

**TwistedScheduler**: use if you’re building a Twisted application

**QtScheduler**: use if you’re building a Qt application

# 3. Ví dụ và tham khảo

Tất cả ví dụ trong folder này hoặc cập nhật [tại đây](https://github.com/agronholm/apscheduler/tree/master/examples)

Tham khảo document và các hướng dẫn khác [tại đây](https://apscheduler.readthedocs.io/en/stable/userguide.html#choosing-the-right-scheduler-job-store-s-executor-s-and-trigger-s)