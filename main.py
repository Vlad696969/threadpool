import threadpool

file_list = ["https://unsplash.com/photos/agzJY5jrsAw/download?force=True",
             "https://unsplash.com/photos/4rDCa5hBlCs/download?force=True",
             "https://unsplash.com/photos/jFCViYFYcus/download?force=True",
             "https://unsplash.com/photos/Y8lCoTRgHPE/download?force=True",
             "https://unsplash.com/photos/4KrQq8Z6Y5c/download?force=True"]

if __name__ == '__main__':
    tp = threadpool.ThreadPool(6)
    tasks = [threadpool.Task(str(i), file_list[i]) for i in range(len(file_list))]
    tp.submit(tasks)
