!!!   gfortran -mcmodel=large -g -fcheck=all -O3 population_bootstrap.f90
!   
!!!   This program calculates the average population form the individual 
!!!   =populations.dat= files kept in the "RESULTS" directory of each trajectories. 
!!!   
!!!   Currently this program only works with the two-state system.
!!!   
!!!   User should modify the path inside the code (it will be eventually read from the  screen)  
!!!   
!!!   
      PROGRAM Population
      IMPLICIT NONE
      integer,parameter :: seed = 42
      integer, parameter :: NSample = 1000       ! Define the number of bootstrap samples

      INTEGER :: NTraj, NTime, kt
      INTEGER :: i, j, ii, jj, k
      INTEGER :: n, io, ierr, IREAD, ios
      INTEGER :: GoodTraj
      INTEGER, ALLOCATABLE :: nl(:)

      REAL :: SimTime, dt 
      REAL :: TT, P1, P2, start, finish,  Totsum, ferr
      REAL, ALLOCATABLE :: Time(:,:), Pop1(:,:), Pop2(:,:)
      REAL, ALLOCATABLE :: TotPop1(:), TotPop2(:)
      REAL, ALLOCATABLE :: GoodTime(:,:), GoodPop1(:,:), GoodPop2(:,:)

      CHARACTER (len=1024) :: format_string 
      CHARACTER (len=1024) :: charI
      CHARACTER (len=1024) :: filename
      character (len=1024) :: path
      character (len=1024) :: command
      character (len=1024) :: temp_file
      character (len=1024) :: header

      integer :: status
      logical :: file_exist
      logical, allocatable :: bad(:)

      integer :: random_index
      real :: sum1, sum2
      real :: BSmean1, BSmean2, BSvar1, BSvar2, BSstd1, BSstd2
      real, allocatable :: BSpop1(:), BSpop2(:)
      real, allocatable :: sample_mean1(:), sample_mean2(:) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      ! Define the temporary file name
!      temp_file = "tempfile.txt"
!
!      ! Build the command depending on the OS
!      command = "pwd > " // temp_file
!
!      ! Execute the command
!      call execute_command_line(command, wait=.true., exitstat=status)
!
!      ! Check if the command was successful
!      if (status == 0) then
!         open(unit=1, file=temp_file, status="old")
!         read(1, '(A)') path
!         close(1)
!         print *, "Current working directory:", trim(adjustl(path))
!      else
!         print *, "Error getting current working directory."
!      endif
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      ! Reading Inputs
      print *, 'Number of Trajectory (must be an integer)'
      read(*, *) NTraj
      print *, 'Total Simulation time (must be a float)'
      read(*, *) SimTime
      print *, 'timestep (must be a float)'
      read(*, *) dt
      print *, 'kt value used in your simulation (must be an integer)'
      read(*, *) kt
      NTime = int(ceiling(SimTime/dt/kt)) + 1 
      write(*,*) SimTime/dt/kt, int(ceiling(SimTime/dt/kt)), NTime
      print *, 'Ntraj =', NTraj
      print *, 'Total Simulation Time =', SimTime
      print *, 'timestep =', dt
      print *, 'kt =', kt
      print *, 'Time array length =', NTime
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      allocate(nl(NTraj))
      allocate(bad(NTraj))
      allocate( Time(NTraj,NTime) )
      allocate( Pop1(NTraj,NTime), Pop2(NTraj,NTime) )
      allocate( TotPop1(NTime), TotPop2(NTime) )
      nl = -99999
      Pop1    = -99999.0D0
      Pop2    = -99999.0D0
      Time    =  0.0D0
      TotPop1 =  0.0D0
      TotPop2 =  0.0D0
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      path = './TRAJECTORIES/'

      call cpu_time(start)
      DO i = 1, NTraj
         IREAD = 1000 + i
         
         if (i < 10) then 
            format_string = "(I1)"
         elseif (i < 100) then
            format_string = "(I2)"
         elseif (i < 1000) then
            format_string = "(I3)"
         else
            format_string = "(I4)"
         endif

         ! For Check the filenames
         write(charI,format_string) i
         !write(*,*) i, trim(path)//'/TRAJ_INSIDE/TRAJ'//trim(charI)// & 
     !&                 '/RESULTS/populations.dat'

         filename = trim(path)//'/TRAJ'//trim(charI)// & 
     &                          '/populations.dat'

         ! Check if the file exists
         inquire(file=filename, exist=file_exist)
         if (.not. file_exist) then
            print *, 'Traj', i, 'file does not exist.'
         else
            ! File exists, so open and read it
            OPEN(unit=IREAD,file=filename,status='old',action='read',iostat=ios)
            if (ios /= 0) then
               print *, 'Error opening file '
            else
               !print *, 'Reading file '

               ! Obtaining the line number of the file 
               n = 0
               DO
                 READ(IREAD, *, iostat=io)
                 IF (io/=0) EXIT
                 n = n + 1
               END DO
               nl(i) = n
               write(*, *) 'Traj',i, 'total lines=',n, nl(i)
               rewind(IREAD)

               ! Second read actually stores the data.
               READ(IREAD,*)
               READ(IREAD,*)
               jj = 1
               DO j = 1, nl(i)-2
                  IF (jj > NTime) THEN
                     EXIT
                  ELSE
                     READ(IREAD,*) TT, ierr, P1, P2
!                     IF ( (TT == 0.0D0) .OR. (MOD(TT,5.0D0) .EQ. 0.0D0) ) THEN
                        Time(i,jj) = TT
                        Pop1(i,jj) = P1
                        Pop2(i,jj) = P2
                        jj = jj + 1
!                     ENDIF
                  ENDIF
               ENDDO
            endif
         endif
      ENDDO
      call cpu_time(finish)
      write(*,*)"Reading Time = ",finish-start," seconds."
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      OPEN(2,File='AVG-ADIAPOP.dat',status='unknown')
      OPEN(3,File='BSAVG-ADIAPOP.dat',status='unknown')
      OPEN(4,File='DATA.csv',access = "sequential", action = "write", &
     &       status = "replace", form = "formatted")

      ! Specify the header
      header = 'Trajectory,Time,Pop1,Pop2'
      write(4, '(A)') trim(header)

      header = '        Time       mean_Pop1        std_Pop1       mean_Pop2        std_Pop2    TotalPop'
      write(3, '(A)') trim(header)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      call cpu_time(start)
      bad = .false.
      n = NTraj
      DO j = 1, NTime
         TotPop1(j) = 0.0d0
         TotPop2(j) = 0.0d0
         DO i = 1, NTraj
            if (.not. bad(i)) then
            IF ( (Pop1(i,j) == -99999.0D0) .OR. & 
     &           (pop2(i,j) == -99999.0D0) ) THEN
               !write(*,*) 'Traj',i,'not included for time =', Time(1,j) 
               bad(i) = .true.
               n = n - 1 
            ELSE 
               ii = i
               TotPop1(j) = TotPop1(j) + Pop1(i,j)
               TotPop2(j) = TotPop2(j) + Pop2(i,j)
            ENDIF 
            endif
         ENDDO
         TotPop1(j) = TotPop1(j)/n
         TotPop2(j) = TotPop2(j)/n
         Totsum = TotPop1(j) + TotPop2(j)
         write(2,'(F12.4, I8, 2F16.8, F12.4)')Time(ii,j),n, & 
     &         TotPop1(j),TotPop2(j),Totsum
      ENDDO
      call cpu_time(finish)
      write(*,*)"Calculation Time = ",finish-start," seconds."
      write(*,*)
      write(*,*)"Incomplete Trajectories:"
      DO i = 1, NTraj
         IF (bad(i)) print *, i
      ENDDO

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      GoodTraj = NTraj - count(bad)
      print *, 'Number of Good Trajectories:', GoodTraj
      allocate(GoodPop1(GoodTraj,NTime),GoodPop2(GoodTraj,NTime))
      allocate(GoodTime(GoodTraj,NTime))

      DO j = 1, NTime
         ii = 1
         DO i = 1, NTraj
            IF (.not.bad(i)) then
               !WRITE(4,*)i, Time(i,j), Pop1(i,j), Pop2(i,j)
               GoodTime(ii,j) = Time(i,j)
               GoodPop1(ii,j) = Pop1(i,j)
               GoodPop2(ii,j) = Pop2(i,j)
               ii = ii + 1
            ENDIF
         ENDDO
      ENDDO
      WRITE(*,*)"Size:",shape(GoodPop1),shape(GoodPop2),shape(GoodTime)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      ! write a csv file
      !do i = 1, GoodTraj
      !   do j = 1, NTime
      !      write(4, 101) i, GoodTime(i,j), GoodPop1(i,j), GoodPop2(i,j)
      !   end do
      !end do
      !close(4)
! 101  format(1x, *(g0, ", ")) 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

      call cpu_time(start)

      allocate(BSpop1(GoodTraj),BSpop2(GoodTraj))
      allocate(sample_mean1(NSample), sample_mean2(NSample))

      ! Initialize random number generator
      call srand(seed)

      ! The Time Loop: everything will be calculated for each time 
      do j = 1, NTime
      
         ! Bootstrap resampling 
         do k = 1, NSample
            do i = 1, GoodTraj
               random_index = int(rand()*GoodTraj) + 1
               !print *,j, k, i, random_index
               BSpop1(i) = GoodPop1(random_index, j)
               BSpop2(i) = GoodPop2(random_index, j)
            end do

            sum1 = 0.0d0
            sum2 = 0.0d0
            do i = 1, GoodTraj
               sum1 = sum1 + BSpop1(i) 
               sum2 = sum2 + BSpop2(i) 
            enddo
            sample_mean1(k) = sum1 / GoodTraj
            sample_mean2(k) = sum2 / GoodTraj
         enddo 
         
         ! Bootstrap mean: Means of sample means
         BSmean1 = 0.0D0
         BSmean2 = 0.0D0
         do k = 1, NSample
            BSmean1 = BSmean1 + sample_mean1(k) 
            BSmean2 = BSmean2 + sample_mean2(k) 
         enddo 
         BSmean1 = BSmean1  / NSample
         BSmean2 = BSmean2  / NSample
 
         ! Bootstrap standard  deviation: Standard deviation of sample means
         BSvar1 = 0.0d0
         BSvar2 = 0.0d0
         do k = 1, NSample
            BSvar1 = BSvar1 + (sample_mean1(k) - BSmean1)**2
            BSvar2 = BSvar2 + (sample_mean2(k) - BSmean2)**2
         enddo 
         BSvar1 = BSvar1 / (GoodTraj -1) 
         BSvar2 = BSvar2 / (GoodTraj -1) 
         BSstd1 = sqrt(BSvar1)
         BSstd2 = sqrt(BSvar2)
   
         write(3,'(F12.4, 4F16.8, F12.4)')GoodTime(random_index,j), & 
     &         BSmean1, BSstd1, BSmean2, BSstd2, (BSmean1+BSmean2)
      enddo 
      
      END PROGRAM Population 

