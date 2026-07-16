options:
  parameters:
    author: ''
    catch_exceptions: 'True'
    category: '[GRC Hier Blocks]'
    cmake_opt: ''
    comment: ''
    copyright: ''
    description: ''
    gen_cmake: 'On'
    gen_linking: dynamic
    generate_options: no_gui
    hier_block_src_path: '.:'
    id: gold_code_transmitter
    max_nouts: '0'
    output_language: python
    placement: (0,0)
    qt_qss_theme: ''
    realtime_scheduling: ''
    run: 'True'
    run_command: '{python} -u {filename}'
    run_options: prompt
    sizing_mode: fixed
    thread_safe_setters: ''
    title: Not titled yet
    window_size: (1000,1000)
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [8, 8]
    rotation: 0
    state: enabled

blocks:
- name: samp_rate
  id: variable
  parameters:
    comment: ''
    value: '4096000'
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [200, 12]
    rotation: 0
    state: enabled
- name: analog_phase_modulator_fc_0
  id: analog_phase_modulator_fc
  parameters:
    affinity: ''
    alias: ''
    comment: ''
    maxoutbuf: '0'
    minoutbuf: '0'
    sensitivity: '1'
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [744, 288.0]
    rotation: 0
    state: enabled
- name: blocks_vector_source_x_0
  id: blocks_vector_source_x
  parameters:
    affinity: ''
    alias: ''
    comment: ''
    maxoutbuf: '0'
    minoutbuf: '0'
    repeat: 'True'
    tags: '[]'
    type: int
    vector: (-1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, 1,
      1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1,
      -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1,
      1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1,
      1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1,
      -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1,
      -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1,
      -1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1,
      -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1,
      1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1,
      -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1,
      -1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1,
      -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1,
      1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1,
      -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1,
      -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1,
      -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1,
      1, 1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1,
      -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1,
      -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1,
      1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1,
      1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1,
      1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1,
      1, -1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1,
      -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1,
      1, -1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1,
      -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1,
      -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1,
      -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1, 1,
      -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1,
      1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1,
      1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1,
      -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1,
      -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1,
      1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1,
      1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1,
      -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, -1,
      1, 1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1,
      -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1,
      -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1,
      -1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1,
      1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, 1, -1,
      -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1,
      -1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1,
      -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, 1, -1,
      -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1, -1, -1,
      -1, 1, -1, 1, -1, 1, -1)
    vlen: '1'
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [184, 256.0]
    rotation: 0
    state: enabled
- name: digital_chunks_to_symbols_xx_0
  id: digital_chunks_to_symbols_xx
  parameters:
    affinity: ''
    alias: ''
    comment: ''
    dimension: '2'
    in_type: int
    maxoutbuf: '0'
    minoutbuf: '0'
    num_ports: '1'
    out_type: float
    symbol_table: '[0, math.pi]'
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [528, 280.0]
    rotation: 0
    state: enabled
- name: import_0
  id: import
  parameters:
    alias: ''
    comment: ''
    imports: import math
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [336, 24.0]
    rotation: 0
    state: enabled
- name: interp_fir_filter_xxx_0
  id: interp_fir_filter_xxx
  parameters:
    affinity: ''
    alias: ''
    comment: ''
    interp: '4'
    maxoutbuf: '0'
    minoutbuf: '0'
    samp_delay: '0'
    taps: ''
    type: ccc
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [920, 280.0]
    rotation: 0
    state: enabled
- name: soapy_hackrf_sink_0
  id: soapy_hackrf_sink
  parameters:
    affinity: ''
    alias: ''
    amp: 'False'
    bandwidth: '0'
    center_freq: '983040000'
    comment: ''
    dev_args: ''
    samp_rate: samp_rate
    type: fc32
    vga: '16'
  states:
    bus_sink: false
    bus_source: false
    bus_structure: null
    coordinate: [1184, 296.0]
    rotation: 0
    state: enabled

connections:
- [analog_phase_modulator_fc_0, '0', interp_fir_filter_xxx_0, '0']
- [blocks_vector_source_x_0, '0', digital_chunks_to_symbols_xx_0, '0']
- [digital_chunks_to_symbols_xx_0, '0', analog_phase_modulator_fc_0, '0']
- [interp_fir_filter_xxx_0, '0', soapy_hackrf_sink_0, '0']

metadata:
  file_format: 1
  grc_version: 3.10.11.0
