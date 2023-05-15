import tekscope

scope = tekscope.TekScope("169.254.155.165")


scope.mkdir('C:/test')

### EXECUTE ONE BLOCK ONLY AT THE TIME

### test first mode: single acquisitions
# scope.mkdir('C:/test/tst1')
# scope.setup_save_traces('C:/test/tst1', 'ALL')
# scope.setup_single_acquisition(5)
# scope.acquisition_start()

### test second mode: averaged acquisitions
# scope.mkdir('C:/test/tst2')
# scope.setup_save_traces('C:/test/tst2', 'ALL')
# scope.setup_average_acquisition(5, 1)
# scope.acquisition_start()

### test other settings
scope.setup_edge_trigger('CH1', 100e-3)

