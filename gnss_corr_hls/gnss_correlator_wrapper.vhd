architecture behavior of gnss_correlator_wrapper is

    -- 1. Declare the component so Vivado knows to look for a black box
    component gnss_correlator is
    port (
        iq_re_TDATA      : IN STD_LOGIC_VECTOR (23 downto 0);
        iq_im_TDATA      : IN STD_LOGIC_VECTOR (23 downto 0);
        code_re_address0 : OUT STD_LOGIC_VECTOR (11 downto 0);
        code_re_ce0      : OUT STD_LOGIC;
        code_re_d0       : OUT STD_LOGIC_VECTOR (23 downto 0);
        code_re_q0       : IN STD_LOGIC_VECTOR (23 downto 0);
        code_re_we0      : OUT STD_LOGIC;
        code_im_address0 : OUT STD_LOGIC_VECTOR (11 downto 0);
        code_im_ce0      : OUT STD_LOGIC;
        code_im_d0       : OUT STD_LOGIC_VECTOR (23 downto 0);
        code_im_q0       : IN STD_LOGIC_VECTOR (23 downto 0);
        code_im_we0      : OUT STD_LOGIC;
        corr_re_TDATA    : OUT STD_LOGIC_VECTOR (23 downto 0);
        corr_im_TDATA    : OUT STD_LOGIC_VECTOR (23 downto 0);
        
        ap_clk           : IN STD_LOGIC;
        ap_rst_n         : IN STD_LOGIC;
        
        iq_re_TVALID     : IN STD_LOGIC;
        iq_re_TREADY     : OUT STD_LOGIC;
        iq_im_TVALID     : IN STD_LOGIC;
        iq_im_TREADY     : OUT STD_LOGIC;
        ap_start         : IN STD_LOGIC;
        corr_re_TVALID   : OUT STD_LOGIC;
        corr_re_TREADY   : IN STD_LOGIC;
        corr_im_TVALID   : OUT STD_LOGIC;
        corr_im_TREADY   : IN STD_LOGIC;
        
        ap_done          : OUT STD_LOGIC;
        ap_ready         : OUT STD_LOGIC;
        ap_idle          : OUT STD_LOGIC
    );
    end component;

begin
    -- 2. Instantiate the component (remove "entity work.")
    uut: gnss_correlator
    port map (
        iq_re_TDATA      => iq_re_TDATA,
        iq_im_TDATA      => iq_im_TDATA,
        code_re_address0 => code_re_address0,
        code_re_ce0      => code_re_ce0,
        code_re_d0       => code_re_d0,
        code_re_q0       => code_re_q0,
        code_re_we0      => code_re_we0,
        code_im_address0 => code_im_address0,
        code_im_ce0      => code_im_ce0,
        code_im_d0       => code_im_d0,
        code_im_q0       => code_im_q0,
        code_im_we0      => code_im_we0,
        corr_re_TDATA    => corr_re_TDATA,
        corr_im_TDATA    => corr_im_TDATA,
        
        ap_clk           => ap_clk,
        ap_rst_n         => ap_rst_n,
        
        iq_re_TVALID     => iq_re_TVALID,
        iq_re_TREADY     => iq_re_TREADY,
        iq_im_TVALID     => iq_im_TVALID,
        iq_im_TREADY     => iq_im_TREADY,
        ap_start         => ap_start,
        corr_re_TVALID   => corr_re_TVALID,
        corr_re_TREADY   => corr_re_TREADY,
        corr_im_TVALID   => corr_im_TVALID,
        corr_im_TREADY   => corr_im_TREADY,
        
        ap_done          => ap_done,
        ap_ready         => ap_ready,
        ap_idle          => ap_idle
    );
end behavior;
