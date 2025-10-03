set print thread-events off
set logging overwrite on
set logging redirect off
set logging on
run
echo \n=== BACKTRACE ==\n
bt
echo \n=== THREADS ==\n
info threads
echo \n=== ALL THREAD BACKTRACE ==\n
thread apply all bt