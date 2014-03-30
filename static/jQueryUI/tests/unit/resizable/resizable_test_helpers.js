TestHelpers.resizable = {
	drag: function( el, dx, dy ) {
		// this mouseover is to work around a limitation in resizable
		$( el ).simulate("mouseover").simulate( "drag", {
			moves: 2,
			dx: dx,
			dy: dy
		});
	}
};